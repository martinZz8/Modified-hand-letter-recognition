import subprocess


def runTrainOfStandardModel(skeletonReceiver,
                            shiftParam,
                            pathToExec,
                            scriptPythonVersion,
                            scriptName,
                            cwd):
    print(f"Started learning model with options:\n"
          f"-skeletonReceiver: {skeletonReceiver},\n"
          f"-shiftParam: {shiftParam}\n")

    # Setup parameters for training model subprocess
    scriptAddParameters = [
        skeletonReceiver,
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
