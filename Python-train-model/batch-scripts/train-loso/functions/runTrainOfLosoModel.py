import subprocess


def runTrainOfLosoModel(skeletonReceiver,
                        personNum,
                        shiftParam,
                        pathToExec,
                        scriptPythonVersion,
                        scriptName,
                        cwd):
    print(f"Started learning model with options:\n"
          f"-skeletonReceiver: {skeletonReceiver},\n"
          f"-personNum: {personNum},\n"
          f"-shiftParam: {shiftParam}\n")

    # Setup parameters for training model subprocess
    scriptAddParameters = [
        skeletonReceiver,
        '-l',
        personNum,
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
