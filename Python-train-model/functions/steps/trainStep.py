from typing import Union
import torch
from timeit import default_timer as timer
from tqdm.auto import tqdm
from functions.countAndPrintElapsedTime import countAndPrintElapsedTime


def trainStep(epochs: int,
              model: torch.nn.Module,
              train_data_loader: torch.utils.data.DataLoader,
              loss_fn: torch.nn.Module,
              optimizer: torch.optim.Optimizer,
              accuracy_fn,
              device: Union[torch.device, str] = "cpu",
              torchManualSeedVal: Union[int, None] = None):
    """Performs a training with a model trying to learn on data_loader."""
    # Set torch seed (if "torchManualSeedVal" is setted)
    if torchManualSeedVal is not None:
        torch.manual_seed(torchManualSeedVal)
        torch.cuda.manual_seed(torchManualSeedVal)

    tracked_values = []

    # Start the timer
    train_time_start_on_device = timer()

    # Put model into training mode
    model.train()

    for epoch in tqdm(range(epochs)):
        # Instantiate the "train_loss" and "train_acc" accumulators for all batches.
        # After that we can divide each accumulator by number of batches, to acquire averaged loss and acc for one epoch.
        train_loss = 0
        train_acc = 0

        # Add a loop to loop through the training batches
        for batchIdx, (X_batch, y_batch) in enumerate(train_data_loader):
            # Turn data into proper device
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)

            # 1. Forward pass
            y_logits = model(X_batch)

            # turn logits -> pred probs -> pred labels
            # Note! We don't have to use "softmax" function in here (can be only "argmax" on "y_logits") - but we can
            y_pred = torch.softmax(y_logits, dim=1).argmax(dim=1)

            # 2. Calculate loss (per batch) + accuracy
            loss = loss_fn(y_logits, y_batch)
            train_loss += loss.item()  # accumulate train loss

            acc = accuracy_fn(y_true=y_batch,
                              y_pred=y_pred)
            train_acc += acc  # accumulate accuracy

            # 3. Optimizer zero grad
            optimizer.zero_grad()

            # 4. Loss backward
            loss.backward()

            # 5. Optimizer step
            optimizer.step()

        # Calc loss and accuracy for single epoch
        calc_loss = train_loss / len(train_data_loader)
        calc_acc = train_acc / len(train_data_loader)

        # Append tracked values
        tracked_values.append({
            "epoch": epoch,
            "loss": calc_loss,
            "acc": calc_acc
        })

    # Stop the timer
    train_time_stop_on_device = timer()

    # Print train time if "print_time" is set to True
    total_train_time_model = countAndPrintElapsedTime(start=train_time_start_on_device,
                                                      end=train_time_stop_on_device,
                                                      device=str(next(model.parameters()).device))

    return tracked_values, total_train_time_model
