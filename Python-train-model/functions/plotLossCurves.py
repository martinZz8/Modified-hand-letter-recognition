import matplotlib.pyplot as plt


def plotLossCurves(tracked_values: list):
    pl_epochs = list(map(lambda x: x["epoch"], tracked_values))
    pl_loss = list(map(lambda x: x["loss"], tracked_values))

    plt.figure(figsize=(7, 7))
    plt.plot(pl_epochs, pl_loss, label="Train loss")
    plt.draw()
    plt.title("Training loss curve")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
