import torch
from timeit import default_timer as timer
from tqdm.auto import tqdm
from functions.countAndPrintElapsedTime import countAndPrintElapsedTime


def trainStep(epochs: int,
              model: torch.nn.Module,
              X_data: torch.Tensor,
              y_data: torch.Tensor,
              loss_fn: torch.nn.Module,
              optimizer: torch.optim.Optimizer,
              accuracy_fn):
    """Performs a training with a model trying to learn on data_loader."""
    tracked_values = []

    # Start the timer
    train_time_start_on_device = timer()

    # Put model into training mode
    model.train()

    for epoch in tqdm(range(epochs)):
        # print(f"Epoch: {epoch}")

        # 1. Forward pass
        y_logits = model(X_data)

        # turn logits -> pred probs -> pred labels
        # Note! We don't have to use "softmax" function in here (can be only "argmax" on "y_logits") - but we can
        y_pred = torch.softmax(y_logits, dim=1).argmax(dim=1)

        # 2. Calculate loss (per batch) + accuracy
        loss = loss_fn(y_logits, y_data)

        acc = accuracy_fn(y_true=y_data,
                          y_pred=y_pred)

        # 3. Optimizer zero grad
        optimizer.zero_grad()

        # 4. Loss backward
        loss.backward()

        # 5. Optimizer step
        optimizer.step()

        # Append tracked values
        tracked_values.append({
            "epoch": epoch,
            "loss": loss.item(),
            "acc": acc
        })

    # Stop the timer
    train_time_stop_on_device = timer()

    # Print train time if "print_time" is set to True
    total_train_time_model = countAndPrintElapsedTime(start=train_time_start_on_device,
                                                      end=train_time_stop_on_device,
                                                      device=str(next(model.parameters()).device))

    return tracked_values, total_train_time_model
