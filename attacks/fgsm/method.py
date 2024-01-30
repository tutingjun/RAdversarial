import torch.optim as optim
import torch
import torch.nn as nn

from .. import AttackMethod

class FGSMMethod(AttackMethod):
    def do_perturbation(self, input_tensor, true_label_idx, epsilon=5.0/255.0, num_iteration = 30) -> AttackMethod:
        # delta = torch.zeros_like(input_tensor, requires_grad=True)
        
        # opt= optim.SGD([delta], lr=1e-1)
        # for t in range(num_iteration):
        #     # normalize
        #     perturbed_input = torch.clamp(input_tensor + delta, 0, 1)
        #     logit = self.model.predict(perturbed_input)
            
        #     label_tensor = torch.LongTensor([true_label_idx]).to(self.model.getDevice())
        #     loss = -nn.CrossEntropyLoss()(logit, label_tensor)
        #     if t % 5 == 0:
        #         print(t, loss.item())
        #     opt.zero_grad()
        #     loss.backward()
        #     opt.step()
        #     delta.data.clamp_(-epsilon, epsilon)
        
        
        # self.perturbed_input = torch.clamp(input_tensor + delta, 0, 1)
        # self.logit = self.model.predict(perturbed_input)
        
        # def fgsm_attack(image, epsilon, data_grad):
        #     # Collect the element-wise sign of the data gradient
        #     sign_data_grad = data_grad.sign()
        #     # Create the perturbed image by adjusting each pixel of the input image
        #     perturbed_image = image + epsilon*sign_data_grad
        #     # Adding clipping to maintain [0,1] range
        #     perturbed_image = torch.clamp(perturbed_image, 0, 1)
        #     # Return the perturbed image
        #     return perturbed_image
        
        # def test( model, device, test_loader, epsilon ):

        # # Accuracy counter
        # correct = 0
        # adv_examples = []

        # # Loop over all examples in test set
        # for data, target in test_loader:

        #     # Send the data and label to the device
        #     data, target = data.to(device), target.to(device)

        #     # Set requires_grad attribute of tensor. Important for Attack
        #     data.requires_grad = True

        #     # Forward pass the data through the model
        #     output = model(data)
        #     init_pred = output.max(1, keepdim=True)[1] # get the index of the max log-probability

        #     # If the initial prediction is wrong, don't bother attacking, just move on
        #     if init_pred.item() != target.item():
        #         continue

        #     # Calculate the loss
        #     loss = F.nll_loss(output, target)

        #     # Zero all existing gradients
        #     model.zero_grad()

        #     # Calculate gradients of model in backward pass
        #     loss.backward()

        #     # Collect ``datagrad``
        #     data_grad = data.grad.data

        #     # Restore the data to its original scale
        #     data_denorm = denorm(data)

        #     # Call FGSM Attack
        #     perturbed_data = fgsm_attack(data_denorm, epsilon, data_grad)

        #     # Reapply normalization
        #     perturbed_data_normalized = transforms.Normalize((0.1307,), (0.3081,))(perturbed_data)

        #     # Re-classify the perturbed image
        #     output = model(perturbed_data_normalized)

        #     # Check for success
        #     final_pred = output.max(1, keepdim=True)[1] # get the index of the max log-probability
        #     if final_pred.item() == target.item():
        #         correct += 1
        #         # Special case for saving 0 epsilon examples
        #         if epsilon == 0 and len(adv_examples) < 5:
        #             adv_ex = perturbed_data.squeeze().detach().cpu().numpy()
        #             adv_examples.append( (init_pred.item(), final_pred.item(), adv_ex) )
        #     else:
        #         # Save some adv examples for visualization later
        #         if len(adv_examples) < 5:
        #             adv_ex = perturbed_data.squeeze().detach().cpu().numpy()
        #             adv_examples.append( (init_pred.item(), final_pred.item(), adv_ex) )

        #     # Calculate final accuracy for this epsilon
        #     final_acc = correct/float(len(test_loader))
        #     print(f"Epsilon: {epsilon}\tTest Accuracy = {correct} / {len(test_loader)} = {final_acc}")

        #     # Return the accuracy and an adversarial example
        #     return final_acc, adv_examples
        
        pass