from os.path import dirname

from functions.runTrainOfLosoModel import runTrainOfLosoModel


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
                runTrainOfLosoModel(sr, perNum, sp, pathToExec, scriptPythonVersion, scriptName, cwd)


if __name__ == "__main__":
    main()
    print("-- END OF SCRIPT --")
