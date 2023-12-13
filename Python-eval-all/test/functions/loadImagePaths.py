import sys
from os.path import isfile, dirname, join
from os import listdir
from tqdm.auto import tqdm

sys.path.append(dirname(__file__))
from consts.consts import availableLetters


def loadImagePaths(inputSingleFolderPath: str):
    loadedImageDicts = []  # list of dictionaries with params "letter" and "path"

    for letter in tqdm(availableLetters[:1]):
        imagesLetterPath = join(inputSingleFolderPath, letter)
        onlyFileNames = [f for f in listdir(imagesLetterPath) if isfile(join(imagesLetterPath, f))]

        for fileName in onlyFileNames:
            imageDict = {
                "letter": letter,
                "imageFileName": fileName,
                "folderPath": imagesLetterPath
            }

            loadedImageDicts.append(imageDict)

    return loadedImageDicts
