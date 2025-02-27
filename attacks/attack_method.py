from PIL import Image
import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F

import os
import sys

import yaml

sys.path.append("..")
from classifiers import TargetModel, label2id, id2label, MobileViTModel
from .utils import create_folders


class AttackMethod:
    def __init__(self, model: TargetModel, config_dict: dict):
        self.model = model
        self.perturbed_input = None
        self.logit = None
        self.number_iteration = None
        self.param_config = config_dict

    def do_perturbation(self, input_tensor: torch.Tensor, label: int) -> "AttackMethod":
        """
        Inherit this class to implement the actual perturbation method
        """
        raise NotImplementedError

    def do_eval(
        self,
        org_img_tensor: torch.Tensor,
        true_label_idx: int,
        topk: int = 5,
        true_target_model=None,
    ) -> "AttackMethod":
        if self.logit is None:
            raise Exception("Must call do_perturbation first")

        if topk < 1 or topk > 5:
            raise Exception("topk must be between 1 and 5")

        # Surrogate models are evaluated on the true target model (MobileViT)
        if true_target_model != None:
            self.model = true_target_model
            org_img_tensor = F.interpolate(
                org_img_tensor, size=(256, 256), mode="bilinear", align_corners=False
            )
            self.perturbed_input = F.interpolate(
                self.perturbed_input, size=(256, 256), mode="bilinear", align_corners=False
            )
            self.logit = self.model.predict(self.perturbed_input)

        # Original Image Prob
        pred = self.model.predict(org_img_tensor)

        # get top 1 prediction from pred
        self.original_top1_index = torch.argmax(pred, dim=1).item()
        self.original_prediction_result = nn.Softmax(dim=1)(pred)[
            0, true_label_idx
        ].item()

        # # Top 1 accuracy
        self.true_class_probability = nn.Softmax(dim=1)(self.logit)[
            0, true_label_idx
        ].item()
        print("True class probability:", self.true_class_probability)

        # Top k accuracy
        topk_indices = torch.topk(self.logit, topk, dim=1)[1].squeeze().tolist()
        topk_indices = [topk_indices] if topk == 1 else topk_indices
        topk_labels = [id2label(idx) for idx in topk_indices]
        topk_probabilities = nn.Softmax(dim=1)(self.logit)[0, topk_indices].tolist()
        print(f"Predicted top {topk} classes: ", topk_labels)
        print(f"Predicted top {topk} probabilities:", topk_probabilities)

        self.topk_indices = topk_indices
        self.topk_labels = topk_labels
        self.topk_probabilities = topk_probabilities

        return self

    def save_eval_to_json(
        self, input_name, true_label_idx, filename: str
    ) -> "AttackMethod":
        if (
            self.topk_indices is None
            or self.topk_labels is None
            or self.topk_probabilities is None
            or self.true_class_probability is None
        ):
            raise Exception("Must call do_eval first")

        if filename[-5:] != ".json":
            raise Exception("Filename must end with .json")

        create_folders(filename)

        import json

        json_dict = {
            "input_name": input_name,
            "true_label": id2label(true_label_idx),
            "true_label_idx": true_label_idx,
            "original_top1_index": self.original_top1_index,
            "original_true_class_probability": self.original_prediction_result,
            "true_class_probability": self.true_class_probability,
            "topk_indices": self.topk_indices,
            "topk_labels": self.topk_labels,
            "topk_probabilities": self.topk_probabilities,
        }

        ## Only for LocSearchAdv
        if self.number_iteration is not None:
            json_dict["num_iteration"] = self.number_iteration

        result_list = None
        if os.path.exists(filename):
            with open(filename, "r") as f:
                result_list = json.load(f)

        if isinstance(result_list, list):
            with open(filename, "w") as f:
                result_list.append(json_dict)
                json.dump(result_list, f)
        else:
            with open(filename, "w") as f:
                json.dump([json_dict], f)

        return self

    def save_perturbation_to_json(self, filename: str) -> "AttackMethod":
        if self.perturbed_input is None:
            raise Exception("Must call do_perturbation first")

        if filename[-5:] != ".json":
            raise Exception("Filename must end with .json")

        create_folders(filename)

        import json

        json_dict = {"perturbed_input": self.perturbed_input.tolist()}

        with open(filename, "w") as f:
            json.dump(json_dict, f)

        return self

    def save_perturbation_to_png(self, filename: str) -> "AttackMethod":
        if self.perturbed_input is None:
            raise Exception("Must call do_perturbation first")

        if filename[-4:] != ".png":
            raise Exception("Filename must end with .png")

        create_folders(filename)

        final_image = (
            self.perturbed_input.squeeze().detach().cpu()
        )  # Remove the batch dimension and move to CPU
        rgb_image = ((final_image) * 255).detach().numpy().transpose(1, 2, 0)
        rgb_image = cv2.cvtColor(
            rgb_image,
            cv2.COLOR_BGR2RGB
        ) if isinstance(self.model, MobileViTModel) else rgb_image

        # Convert the numpy array to a PIL image
        pil_image = Image.fromarray(rgb_image.astype("uint8"))

        # Save the image as png
        pil_image.save(filename)

        return self
