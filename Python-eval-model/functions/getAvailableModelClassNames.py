from os import listdir
from os.path import join, dirname, isfile


# Note! Model class names are same as their files (of course without extension)
# Note2! "__file__" is current absolute path to file to this function. "dirname" function from "os.path" module gets absolute path to parent directory of file passed as parameter
def getAvailableModelClassNames() -> list[str]:
    pathToModelClasses = join(
        dirname(
            dirname(
                (dirname(__file__))
            )
        ),
        "Python-train-model", "models"
    )

    # Search for files that are inside "pathToModelClasses" location
    innerFiles = [f
                  for f in listdir(pathToModelClasses)
                  if isfile(join(pathToModelClasses, f))
                  ]

    innerFilesWOExt = []

    # Get file names without extensions
    for innerFile in innerFiles:
        splittedFileName = innerFile.split(".")

        if len(splittedFileName) > 1:
            innerFilesWOExt.append(splittedFileName[0])

    return innerFilesWOExt
