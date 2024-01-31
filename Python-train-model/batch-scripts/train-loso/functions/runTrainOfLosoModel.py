import subprocess


def runTrainOfLosoModel(skeletonReceiver: str,
                        datasetVersion: int,
                        personNum: int,
                        shiftParam: str,
                        pathToExec: str,
                        scriptPythonVersion: str,
                        scriptName: str,
                        cwd: str):
    print(f"Started learning model with options:\n"
          f"-skeletonReceiver: {skeletonReceiver},\n"
          f"-personNum: {personNum},\n"
          f"-shiftParam: {shiftParam}\n")

    # Setup parameters for training model subprocess
    scriptAddParameters = [
        skeletonReceiver,
        '-v',
        str(datasetVersion),
        '-l',
        str(personNum),
        shiftParam,
        '-G'
    ]

    # -- Run subprocess --
    ls_output = subprocess.Popen([pathToExec, scriptPythonVersion, scriptName] + scriptAddParameters, cwd=cwd)
    ls_output.communicate()
    rc = ls_output.returncode

    if rc == 0:
        print("Successfully learned model.")
    else:
        print("There was error during learning model.")
