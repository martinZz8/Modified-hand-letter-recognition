import sys
from os.path import dirname, join
import subprocess


def performTest(selectedOptionList, imagePath, currLosoPersonNum: int = None, resultFileName="results.txt"):
    # Specify output params
    errorTermination = True
    predictedLetter = "-"
    properClassify = False
    resultFilePath = ""

    # Prepare params to run classify script
    pathToExec = "py"
    scriptPythonVersion = "-3"
    scriptName = "main-single.py"
    scriptAddParameters = selectedOptionList + [
        '-f',
        imagePath['folderPath'],
        '-i',
        imagePath['imageFileName'],
        '-t',
        resultFileName,
        '-l' if currLosoPersonNum is not None else '',
        str(currLosoPersonNum) if currLosoPersonNum is not None else ''
    ]
    scriptAddParameters = list(filter(lambda x: len(x) > 0, scriptAddParameters))

    cwd = join(dirname(dirname(dirname(__file__))), "single-classify")

    # -- Run "main-single.py" script --
    ls_output = subprocess.Popen([pathToExec, scriptPythonVersion, scriptName] + scriptAddParameters, cwd=cwd)
    ls_output.communicate()  # Will block for 30 seconds
    rc = ls_output.returncode
    # print(f"rc: {rc}")

    # Check whether script terminated successfully (without error) and check for result
    if rc == 0:
        errorTermination = False
        resultFilePath = join(cwd, "output", resultFileName)

        # Check for result
        with open(resultFilePath, "r") as f:
            resultFileContent = f.read()
            resultFileContentLines = resultFileContent.split("\n")

            if len(resultFileContentLines) > 0:
                predictedLetter = resultFileContentLines[0].split(": ")[1]
                # print(f"Predicted letter: {predictedLetter}")

                if predictedLetter == imagePath['letter']:
                    properClassify = True

    return {
        'errorTermination': errorTermination,
        'realLetter': imagePath['letter'],
        'predictedLetter': predictedLetter,
        'properClassify': properClassify,
        'resultFilePath': resultFilePath
    }
