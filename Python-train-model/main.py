# Standard imports
import sys
import getopt
import torch
from torch import nn
import matplotlib.pyplot as plt
from functions.loadData import loadData
from functions.splitTrainTestData import splitTrainTestData
from functions.plotLossCurves import plotLossCurves
from functions.plotAccuracy import plotAccuracy
from functions.accuracyFn import accuracyFn
from functions.saveModelToFile import saveModelToFile
from functions.combineAdditionalModelTestData import combineAdditionalModelTestData

# Train and test steps
from functions.steps.trainStep import trainStep
from functions.steps.testStep import testStep

# Model imports
from models.MediaPipeShiftedModelV1 import MediaPipeShiftedModelV1


def main(argv):
    # --Variables--
    availableLetters = ['A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'L', 'M', 'N', 'O', 'P', 'R', 'W', 'Y']

    # -- Inner option variables --
    testDataFactor = 0.1
    torchManualSeedVal = -1

    # --Option variables--
    useMediaPipe = True
    useShiftedData = True
    useCuda = True

    # --Read input arguments and set variables--
    # Note:
    # - each option consists of key and value pair
    # - to use short option, write hyphen followed by letter (and then space and value), e.g. "-i info.txt"
    # - to use long option, write double hyphen followed by string (and then space and value), e.g. "--long-option info.txt"

    # Also note, that in second argument of "getopt.getopt()" method (short args) you should provice colon ':' after short argument, if it's with value, otherwise no.
    # Same thing goes to third argument (long args), but with equal sign '='.
    opts, args = getopt.getopt(argv, "hmosScC",
                               ["help", "media-pipe", "open-pose", "shifted-data", "no-shifted-data", "cuda", "cpu"])

    for opt, arg in opts:
        if opt in ("-h", "--help"):  # help
            print('Available options:\n'
                  '-h, --help (help)\n'
                  '-m, --media-pipe (use MediaPipe - default)\n'
                  '-o, --open-pose (use OpenPose)\n'
                  '-s, --shifted-data (use shifted data - default)\n'
                  '-S, --no-shifted-data (use non-shifted data)\n'
                  '-c, --cuda (use cuda if available - default)\n'
                  '-C, --cpu (use cpu)\n\n'
                  'Also note, that you should use only one of the following pair values (otherwise it would be used the least provided):\n'
                  '-m, -o\n'
                  '-s, -S\n'
                  '-c, -C')
            sys.exit()
        elif opt in ("-m", "--media-pipe"):  # use MediaPipe data - default
            useMediaPipe = True
        elif opt in ("-o", "--open-pose"):  # use OpenPose data
            useMediaPipe = False
        elif opt in ("-s", "--shifted-data"):  # use shifted data - default
            useShiftedData = True
        elif opt in ("-S", "--no-shifted-data"):  # use non-shifted data
            useShiftedData = False
        elif opt in ("-c", "--cuda"):  # use cuda if available - default
            useCuda = True
        elif opt in ("-C", "--cpu"):  # use cpu
            useCuda = False

    print(f"Used options:\n"
          f"- useMediaPipe = {useMediaPipe}\n"
          f"- useShiftedData = {useShiftedData}\n"
          f"- useCuda = {useCuda}")

    # --Set device agnostic code (if user wants to and it's available)--
    deviceStr = "cpu"
    if useCuda and torch.cuda.is_available():
        deviceStr = "cuda"
    else:
        print(f"WARNING: CUDA isn't used, since it's unavailable on this device. Using CPU.")

    # --Load data--
    print("1. Loading data ...")
    loadedData = loadData(useMediaPipe, useShiftedData, availableLetters)
    # print(f"loadedData: {len(loadedData), len(loadedData[0]), len(loadedData[0][0]), len(loadedData[0][0][0])}")

    # -- Split data into training and testing values --
    XTrain, YTrain, XTest, YTest, allDrawnTestIdxs = splitTrainTestData(loadedData, testDataFactor, True)
    # print(f"XTrain: {len(XTrain)}\nYTrain: {len(YTrain)}\nXTest: {len(XTest)}\nYTest: {len(YTest)}")
    # print(f"allDrawnTestIdxs: {allDrawnTestIdxs}")

    # -- Turn data into tensors --
    XTrainTen = torch.tensor(XTrain).to(deviceStr)
    YTrainTen = torch.tensor(YTrain).to(deviceStr)
    XTestTen = torch.tensor(XTest).to(deviceStr)
    YTestTen = torch.tensor(YTest).to(deviceStr)

    # -- Create model --
    if torchManualSeedVal != -1:
        torch.manual_seed(torchManualSeedVal)
        torch.cuda.manual_seed(torchManualSeedVal)

    modelMediaPipeShiftedV1 = MediaPipeShiftedModelV1(
        input_shape=len(XTrain[0]) * len(XTrain[0][0]),
        hidden_units=30,
        output_shape=len(availableLetters)
    ).to(deviceStr)

    lossFn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(params=modelMediaPipeShiftedV1.parameters(),
                                lr=0.0001)

    # -- Perform train step --
    print("2. Training model ...")
    # Set the number of epochs
    epochs = 15000

    # Perform training loop
    if torchManualSeedVal != -1:
        torch.manual_seed(torchManualSeedVal)
        torch.cuda.manual_seed(torchManualSeedVal)

    tracked_train_values, total_train_time = trainStep(
        epochs,
        modelMediaPipeShiftedV1,
        XTrainTen,
        YTrainTen,
        lossFn,
        optimizer,
        accuracyFn
    )

    # Print last accuracy
    print(f"Last train acc: {tracked_train_values[-1]['acc']}")

    # -- Plot results --
    # Plot the loss curves
    plotLossCurves(tracked_train_values)

    # Plot the accuracy
    plotAccuracy(tracked_train_values)

    # -- Perform test step --
    print("3. Testing model ...")
    if torchManualSeedVal != -1:
        torch.manual_seed(torchManualSeedVal)
        torch.cuda.manual_seed(torchManualSeedVal)

    tracked_test_values = testStep(
        modelMediaPipeShiftedV1,
        XTestTen,
        YTestTen,
        lossFn,
        accuracyFn
    )

    print(f"tracked_test_values:\n"
          f"- model_name: {tracked_test_values['model_name']}\n"
          f"- loss: {tracked_test_values['loss']}\n"
          f"- acc: {tracked_test_values['acc']}")

    # -- Perform model save --
    print("4. Saving model to file ...")
    # Save model to file and folder with specified name
    outputDirName = "outputModels"
    modelNameToSave = "HSRecModel_"
    modelExtensionName = ".pth"

    if useMediaPipe:
        modelNameToSave += "M"
    else:
        modelNameToSave += "O"

    if useShiftedData:
        modelNameToSave += "S"
    else:
        modelNameToSave += "O"

    # Save model
    statisticsStr = f"Model name: {modelNameToSave}\n\n" \
                    f"Basic data:\n" \
                    f"a) train ({epochs} epochs in {total_train_time:.2f} sec - cuda {'' if useCuda else 'not'} used):\n" \
                    f"- loss: {tracked_train_values[-1]['loss']:.2f}\n" \
                    f"- acc: {tracked_train_values[-1]['acc']:.2f}%\n\n" \
                    f"b) test:\n" \
                    f"- loss: {tracked_test_values['loss']:.2f}\n" \
                    f"- acc: {tracked_test_values['acc']:.2f}%"

    additionalTestDataStr = combineAdditionalModelTestData(allDrawnTestIdxs,
                                                           tracked_test_values["y_true"],
                                                           tracked_test_values["y_pred"],
                                                           availableLetters)

    saveModelToFile(modelMediaPipeShiftedV1,
                    outputDirName,
                    modelNameToSave,
                    modelExtensionName,
                    statisticsStr,
                    additionalTestDataStr)


if __name__ == "__main__":
    main(sys.argv[1:])
    print("-- END OF SCRIPT --")
    # -- Show plots --
    plt.show()
