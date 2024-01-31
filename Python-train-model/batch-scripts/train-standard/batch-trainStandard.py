from os.path import dirname
from functions.runTrainOfStandardModel import runTrainOfStandardModel
from functions.doesModelFolderExists import doesModelFolderExists
from functions.determineUsedDatasetVersion import determineUsedDatasetVersion


def main():
    # --Consts--
    skeletonReceivers = ["-m", "-o"]
    shiftParams = ["-s", "-S"]
    mediaPipeDatasetVersion = 1
    openPoseDatasetVersion = 2

    # Setup some parameters for training model subprocess
    pathToExec = "py"
    scriptPythonVersion = "-3"
    scriptName = "main.py"

    cwd = dirname(dirname(dirname(__file__)))

    for sr in skeletonReceivers:
        for sp in shiftParams:
            usedDatasetVersion = determineUsedDatasetVersion(sr, mediaPipeDatasetVersion, openPoseDatasetVersion)

            if doesModelFolderExists(sr, sp):
                print(f"Bypass of model train with params:\n"
                      f"- skeletonReceiver: {sr}\n"
                      f"- datasetVersion: {usedDatasetVersion}\n"
                      f"- shiftParam: {sp}")
                continue
            runTrainOfStandardModel(sr,
                                    usedDatasetVersion,
                                    sp,
                                    pathToExec,
                                    scriptPythonVersion,
                                    scriptName,
                                    cwd)


if __name__ == "__main__":
    main()
    print("-- END OF SCRIPT --")
