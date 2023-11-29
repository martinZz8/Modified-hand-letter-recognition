# Standard imports
from typing import Union
import sys
import torch

sys.path.append("../Python-train-model")  # Needed to run this script properly from CMD
# Custom consts imports
from consts.consts import availableLetters

# Custom functions imports
from functions.getArgumentOptionsEval import getArgumentOptionsEval
from functions.loadModelObject import loadModelObject
from functions.getAvailableModelClassNames import getAvailableModelClassNames
from functions.loadInputSkeleton import loadInputSkeleton
from functions.steps.evalStep import evalStep
from functions.saveEvalResultsToFile import saveEvalResultsToFile

# Import models
from models.UniversalModelV1 import UniversalModelV1


def main(argv):
    # --Consts--
    inputFolderName: str = "input"
    outputFolderName: str = "output"

    # -- Inner option variables --
    torchManualSeedVal: Union[int, None] = None  # default: None

    # --Option variables--
    useMediaPipe: bool = True  # default: True
    useShiftedData: bool = True  # default: True
    modelVersion: int = 1  # default: 1
    modelClassName: str = "UniversalModelV1"  # default: "UniversalModelV1"
    inputSkeletonFileName: str = "inputSkeletonMS_A6.txt"  # default: "inputSkeletonMS_A6.txt"
    outputFileName: str = ""  # default: "" stands for auto incremented file name
    useCuda: bool = False  # default: False - it's faster for single evaluation to use CPU than GPU (moving data to GPU - CUDA costs more than evaluation benefits gained from it)

    # --Read input arguments and set variables--
    useMediaPipe, useShiftedData, modelVersion, modelClassName, inputSkeletonFileName, outputFileName, useCuda = getArgumentOptionsEval(argv,
                                                                                                                                        useMediaPipe,
                                                                                                                                        useShiftedData,
                                                                                                                                        modelVersion,
                                                                                                                                        modelClassName,
                                                                                                                                        inputSkeletonFileName,
                                                                                                                                        outputFileName,
                                                                                                                                        useCuda)
        # --Set device agnostic code (if user wants to and it's available)--
    deviceStr = "cpu"
    if useCuda and torch.cuda.is_available():
        deviceStr = "cuda"
    else:
        print(f"WARNING: CUDA isn't used{', since its unavailable on this device' if (not torch.cuda.is_available()) and useCuda else ''}. Using CPU.")

    # --Loading input skeleton to classify--
    print("1. Loading input skeleton to classify ...")
    inputSkeleton = loadInputSkeleton(inputFolderName, inputSkeletonFileName)
    XTen = torch.tensor(inputSkeleton).unsqueeze(0)  # Note! We have to "unsqueeze(0)" this data, since we have here only one row to predict (it has t obe in shape list of rows)

    # --Recreate model from loaded model object--
    print("2. Loading model ...")
    availableModelClassNames = getAvailableModelClassNames()

    if modelClassName not in availableModelClassNames:
        raise Exception("Wrong input argument '-n' or '--model-class-name'. Use '-h' to see available values.")

    model = None

    # Get model based on passed "modelClassName" parameter
    if torchManualSeedVal is not None:
        torch.manual_seed(torchManualSeedVal)
        torch.cuda.manual_seed(torchManualSeedVal)

    if modelClassName == "UniversalModelV1":
        model = UniversalModelV1(
            input_shape=42,
            output_shape=len(availableLetters)
        )
    # ... Place other "elseif" statements, when more model classes will appear

    if model is None:
        raise Exception("Model is 'None'")

    # Load desired model object
    modelObject, modelObjectFolderName = loadModelObject(useMediaPipe, useShiftedData, modelVersion)

    # Insert loaded model object into our model. Also change device type
    model.load_state_dict(modelObject)
    model.to(deviceStr)

    # --Evaluate model--
    print("3. Evaluate model ...")
    tracked_eval_values = evalStep(
        model,
        XTen,
        deviceStr,
        torchManualSeedVal
    )

    print(f"tracked_eval_values:\n"
          f"- model_name: {tracked_eval_values['model_name']}\n"
          f"- y_single_pred: {tracked_eval_values['y_single_pred']}\n"
          f"- total_eval_time_model: {tracked_eval_values['total_eval_time_model']:.2f} sec")

    print(f"Predicted letter: {availableLetters[tracked_eval_values['y_single_pred']]}")

    # -- Save results to file --
    print("5. Saving results to file ...")
    # TODO - prepare statistics str (with model_name, predicted letter and time)
    statisticsStr = f"Recognized class: {availableLetters[tracked_eval_values['y_single_pred']]}\n" \
                    f"Evaluation time (with {'CUDA' if useCuda else 'CPU'}): {tracked_eval_values['total_eval_time_model']:.2f} sec\n" \
                    f"Input file name: {inputSkeletonFileName}\n" \
                    f"Used trained model name: {modelObjectFolderName}\n" \
                    f"Used model class name: {modelClassName}"

    savedIntoFileName = saveEvalResultsToFile(outputFolderName,
                                              outputFileName,
                                              statisticsStr)

    print(f"Saved results into file with name: {savedIntoFileName}")


if __name__ == "__main__":
    main(sys.argv[1:])
    print("-- END OF SCRIPT --")
