import sys
from os.path import dirname, join
from functions.runTrainOfLosoModel import runTrainOfLosoModel

sys.path.append(join(dirname(dirname(__file__)), "train-standard"))
from functions.doesModelFolderExists import doesModelFolderExists


def main():
    # --Consts--
    skeletonReceivers = ["-m", "-o"]
    personNums = [str(x) for x in range(1, 13)]
    shiftParams = ["-s", "-S"]

    # Setup some parameters for training model subprocess
    pathToExec = "py"
    scriptPythonVersion = "-3"
    scriptName = "main.py"

    cwd = dirname(dirname(dirname(__file__)))

    for sr in skeletonReceivers:
        for perNum in personNums:
            for sp in shiftParams:
                if doesModelFolderExists(sr, sp, perNum):
                    print(f"Bypass of model train with params:\n"
                          f"- skeletonReceiver: {sr}\n"
                          f"- shiftParam: {sp}\n"
                          f"- personNum: {perNum}")
                    continue
                runTrainOfLosoModel(sr, perNum, sp, pathToExec, scriptPythonVersion, scriptName, cwd)


if __name__ == "__main__":
    main()
    print("-- END OF SCRIPT --")
