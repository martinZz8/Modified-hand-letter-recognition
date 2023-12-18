def checkIfOutputIsProper(pathToOutputFile: str):
    with open(pathToOutputFile, "r") as file:
        fileContent = file.read()
        splittedFileContent = fileContent.split("\n")

        lenOfSplittedFileContent = len(splittedFileContent)
        if lenOfSplittedFileContent != 22:
            return False, lenOfSplittedFileContent

        return True, lenOfSplittedFileContent
