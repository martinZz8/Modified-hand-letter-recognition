import sys
from os.path import dirname

sys.path.append(dirname(dirname(__file__)))
from exceptions.ErrorInputFileLetter import ErrorInputFileLetter

sys.path.append(dirname(dirname(dirname(__file__))))
from consts.consts import availableLetters

def getLettersFromListStr(listStr: str):
    splittedListStr = list(
        map(
            lambda x: x.replace("[", "").replace("]", ""),
            listStr.split(": ")[1].split(", ")
        )
    )

    liToRet = []
    for chStr in splittedListStr:
        if not (chStr in availableLetters) and chStr != "-":
            raise ErrorInputFileLetter(f"Error - output file contains not supported letter {chStr}.")
        else:
            liToRet.append(chStr)

    return liToRet
