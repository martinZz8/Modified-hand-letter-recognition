def replaceCharactersInFile(filePath: str,
                            characterToReplace: str,
                            characterToReplaceWith: str,
                            removeBlankLines: bool = True):
    # Read skeleton from file
    with open(filePath, "r") as file:
        fileContent = file.read()

    # Filter out blank lines (e.g. last line in OpenPose skeleton files is blank)
    if removeBlankLines:
        filteredFileContentRows = list(
            filter(
                lambda x: len(x) > 0,
                fileContent.split("\n")
            )
        )
        fileContent = "\n".join(filteredFileContentRows)

    # Replace characters with new one
    fileContent = fileContent.replace(characterToReplace, characterToReplaceWith)

    # Save changed skeleton to file
    with open(filePath, "w") as file:
        file.write(fileContent)
