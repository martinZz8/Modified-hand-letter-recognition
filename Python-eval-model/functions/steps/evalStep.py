from typing import Union
import torch
from timeit import default_timer as timer
from functions.countAndPrintElapsedTime import countAndPrintElapsedTime


def evalStep(model: torch.nn.Module,
             X_data: torch.Tensor,
             device: Union[torch.device, str] = "cpu",
             torchManualSeedVal: Union[int, None] = None):
    """Returns a dictionary containing the results of model evaluating/predicting on "X_data."""
    # Set torch seed (if "torchManualSeedVal" is setted)
    if torchManualSeedVal is not None:
        torch.manual_seed(torchManualSeedVal)
        torch.cuda.manual_seed(torchManualSeedVal)

    # Turn data into proper device
    X_data = X_data.to(device)

    # Start the timer
    eval_time_start_on_device = timer()

    # Put model into testing mode
    model.eval()

    # Turn on inference mode context manager
    with torch.inference_mode():
        y_logits = model(X_data)

        # turn logits -> pred probs -> pred labels
        y_single_pred = torch.softmax(y_logits, dim=1).argmax(dim=1).item()

    # Stop the timer
    eval_time_stop_on_device = timer()

    # Print train time if "print_time" is set to True
    total_eval_time_model = countAndPrintElapsedTime(start=eval_time_start_on_device,
                                                     end=eval_time_stop_on_device,
                                                     device=str(next(model.parameters()).device))

    return {
        "model_name": model.__class__.__name__,  # only works when model was created with a class
        "y_single_pred": y_single_pred,
        "total_eval_time_model": total_eval_time_model
    }
