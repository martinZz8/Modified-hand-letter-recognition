import matplotlib.pyplot as plt


def plotAccuracy(tracked_values: list):
    pl_epochs = list(map(lambda x: x["epoch"], tracked_values))
    pl_acc = list(map(lambda x: x["acc"], tracked_values))

    plt.figure(figsize=(7, 7))
    plt.plot(pl_epochs, pl_acc, label="Train accuracy")
    plt.draw()
    plt.title("Train accuracy")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()
