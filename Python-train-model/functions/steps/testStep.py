from typing import Union
import torch


def testStep(model: torch.nn.Module,
             X_test_data: torch.Tensor,
             y_test_data: torch.Tensor,
             loss_fn: torch.nn.Module,
             accuracy_fn,
             device: Union[torch.device, str] = "cpu",
             torchManualSeedVal: Union[int, None] = None):
    """Returns a dictionary containing the results of model predicting on "X_test_data"."""
    # Set torch seed (if "torchManualSeedVal" is setted)
    if torchManualSeedVal is not None:
        torch.manual_seed(torchManualSeedVal)
        torch.cuda.manual_seed(torchManualSeedVal)

    # Turn data into proper device
    X_test_data, y_test_data = X_test_data.to(device), y_test_data.to(device)

    # Put model into testing mode
    model.eval()

    # Turn on inference mode context manager
    with torch.inference_mode():
        y_logits = model(X_test_data)

        # turn logits -> pred probs -> pred labels
        y_test_pred = torch.softmax(y_logits, dim=1).argmax(dim=1)

        loss = loss_fn(y_logits, y_test_data)

        acc = accuracy_fn(y_true=y_test_data,
                          y_pred=y_test_pred)

    # print(f"For testing, the loss is: {calc_loss}, acc is: {calc_acc}")
    return {
        "model_name": model.__class__.__name__,  # only works when model was created with a class
        "loss": loss.item(),
        "acc": acc,
        "y_true": y_test_data,
        "y_pred": y_test_pred
    }
