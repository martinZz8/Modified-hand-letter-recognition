# Standard imports
from typing import Union
import sys
import torch
from torch import nn
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# Custom consts imports
from consts.consts import availableLetters

# Custom functions imports
from functions.getArgumentOptions import getArgumentOptions
from functions.loadData import loadData
from functions.splitTrainTestData import splitTrainTestData
from functions.plotLossCurves import plotLossCurves
from functions.plotAccuracy import plotAccuracy
from functions.accuracyFn import accuracyFn
from functions.saveModelToFile import saveModelToFile
from functions.combineAdditionalModelTestData import combineAdditionalModelTestData
from functions.determineBestModel import determineBestModel

# Custom train and test steps imports
from functions.steps.trainStep import trainStep
from functions.steps.testStep import testStep

# Model imports
from models.UniversalModelV1 import UniversalModelV1


def main(argv):
    # --Variables--
    # Note! (Variable moved to "consts/consts.py" file)
    # availableLetters: list[str] = ['A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'L', 'M', 'N', 'O', 'P', 'R', 'W', 'Y']

    # -- Inner option variables --
    testDataFactor: float = 0.1  # default: 0.1
    torchManualSeedVal: Union[int, None] = None  # default: None
    trainEpochs: int = 15000  # default: 15000
    trainBatchSize: int = 16  # default: 16
    optimizerLearningRate: float = 0.0001  # default: 0001

    # --Option variables--
    useMediaPipe: bool = True  # default: True
    useShiftedData: bool = True  # default: True
    losoPersonTester: int = -1  # default: -1
    useCuda: bool = True  # default: True
    modelRepeats: int = 1  # default: 1
    showGraphs: bool = True  # default: True

    # --Read input arguments and set variables--
    useMediaPipe, useShiftedData, losoPersonTester, useCuda, modelRepeats, showGraphs = getArgumentOptions(argv,
                                                                                                           useMediaPipe,
                                                                                                           useShiftedData,
                                                                                                           losoPersonTester,
                                                                                                           useCuda,
                                                                                                           modelRepeats,
                                                                                                           showGraphs)

    # --Set device agnostic code (if user wants to and it's available)--
    deviceStr = "cpu"
    if useCuda and torch.cuda.is_available():
        deviceStr = "cuda"
    else:
        print(f"WARNING: CUDA isn't used{', since its unavailable on this device' if (not torch.cuda.is_available()) and useCuda else ''}. Using CPU.")

    # --Load data--
    print("1. Loading data ...")
    loadedData = loadData(useMediaPipe, useShiftedData, availableLetters)
    # print(f"loadedData: {len(loadedData), len(loadedData[0]), len(loadedData[0][0]), len(loadedData[0][0][0])}")

    # -- Perform model repeats "modelRepeats" times
    allModelDatas = []

    for i in range(modelRepeats):
        print(f"** Model repeat number: {i + 1}**")

        # -- Split data into training and testing values --
        # Note! We also shuffle train and test data (3rd parameter is set to True)
        XTrain, YTrain, XTest, YTest, allDrawnTestIdxs = splitTrainTestData(loadedData, losoPersonTester, testDataFactor, True)
        # print(f"XTrain: {len(XTrain)}\nYTrain: {len(YTrain)}\nXTest: {len(XTest)}\nYTest: {len(YTest)}")
        # print(f"allDrawnTestIdxs: {allDrawnTestIdxs}")

        # -- Turn train data into iterable batches --
        # Create list of 2d tuples (where first element of tuple has tensor, second has scalar value)
        # e.g. inputOfDataLoader = [(tensor([1,2,3], 1)), (torch.tensor([4,5,6]), 2)]
        # After that, paste it into "DataLoader" class to create iterable batches for training
        inputOfDataLoader = list(zip([torch.Tensor(singleX) for singleX in XTrain], YTrain))
        trainDataLoader = DataLoader(dataset=inputOfDataLoader,
                                     batch_size=trainBatchSize,
                                     shuffle=False)

        # -- Turn data into tensors --
        # XTrainTen = torch.tensor(XTrain) #.to(deviceStr)
        # YTrainTen = torch.tensor(YTrain) #.to(deviceStr)
        XTestTen = torch.tensor(XTest)  # ".to(deviceStr)" is performed inside "testStep" method
        YTestTen = torch.tensor(YTest)  # ".to(deviceStr)" is preformed inside "testStep" method

        # -- Create model --
        if torchManualSeedVal is not None:
            torch.manual_seed(torchManualSeedVal)
            torch.cuda.manual_seed(torchManualSeedVal)

        modelV1 = UniversalModelV1(
            input_shape=len(XTrain[0]) * len(XTrain[0][0]),
            output_shape=len(availableLetters)
        ).to(deviceStr)

        lossFn = nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(params=modelV1.parameters(),
                                    lr=optimizerLearningRate)

        # -- Perform train step --
        print("2. Training model ...")

        # Perform training loop
        tracked_train_values_li, total_train_time = trainStep(
            trainEpochs,
            modelV1,
            trainDataLoader,
            lossFn,
            optimizer,
            accuracyFn,
            deviceStr,
            torchManualSeedVal
        )

        # Print last accuracy
        print(f"Last train acc: {tracked_train_values_li[-1]['acc']}")

        # -- Perform test step --
        print("3. Testing model ...")

        tracked_test_values = testStep(
            modelV1,
            XTestTen,
            YTestTen,
            lossFn,
            accuracyFn,
            deviceStr,
            torchManualSeedVal
        )

        print(f"tracked_test_values:\n"
              f"- model_name: {tracked_test_values['model_name']}\n"
              f"- loss: {tracked_test_values['loss']}\n"
              f"- acc: {tracked_test_values['acc']}")

        # -- Append model data into "allModelDatas" list --
        allModelDatas.append({
            "model": modelV1,
            "tracked_train_values_li": tracked_train_values_li,
            "tracked_test_values": tracked_test_values,
            "total_train_time": total_train_time,
            "allDrawnTestIdxs": allDrawnTestIdxs
        })

        if i != (modelRepeats - 1):
            print("\n")

    # -- Determining best model from all models inside "allModelDatas" list
    print("4. Determining best model ...")
    bestModelData = determineBestModel(allModelDatas)

    if bestModelData is not None:
        if showGraphs:
            # -- Plot best results --
            # Plot the loss curves
            plotLossCurves(bestModelData["tracked_train_values_li"])

            # Plot the accuracy
            plotAccuracy(bestModelData["tracked_train_values_li"])

        # -- Perform best model save --
        print("5. Saving best model to file ...")

        # Save model to file and folder with specified name
        outputDirName = "outputModels"
        modelNameToSave = "HSRecModel_"
        modelExtensionName = ".pth"

        if losoPersonTester > -1:
            modelNameToSave += f"LOSO_{losoPersonTester}_"

        if useMediaPipe:
            modelNameToSave += "M"
        else:
            modelNameToSave += "O"

        if useShiftedData:
            modelNameToSave += "S"
        else:
            modelNameToSave += "O"

        # Save model with additional data to files
        statisticsStr = f"Model name: {modelNameToSave}\n\n" \
                        f"Basic data:\n" \
                        f"a) train ({trainEpochs} epochs in {bestModelData['total_train_time']:.2f} sec - cuda {'' if useCuda else 'not'}used):\n" \
                        f"- loss: {bestModelData['tracked_train_values_li'][-1]['loss']:.2f}\n" \
                        f"- acc: {bestModelData['tracked_train_values_li'][-1]['acc']:.2f}%\n\n" \
                        f"b) test:\n" \
                        f"- loss: {bestModelData['tracked_test_values']['loss']:.2f}\n" \
                        f"- acc: {bestModelData['tracked_test_values']['acc']:.2f}%"

        additionalTestDataStr = combineAdditionalModelTestData(bestModelData['allDrawnTestIdxs'],
                                                               bestModelData['tracked_test_values']["y_true"],
                                                               bestModelData['tracked_test_values']["y_pred"],
                                                               availableLetters)

        savedIntoFolderName = saveModelToFile(bestModelData["model"],
                                              outputDirName,
                                              modelNameToSave,
                                              modelExtensionName,
                                              statisticsStr,
                                              additionalTestDataStr)
        print(f"Saved data into folder with name: {savedIntoFolderName}")
    else:
        print("ERROR: Couldn't determine best model. No data was saved into files.")


if __name__ == "__main__":
    main(sys.argv[1:])
    print("-- END OF SCRIPT --")

    # -- Show plots --
    plt.show()
