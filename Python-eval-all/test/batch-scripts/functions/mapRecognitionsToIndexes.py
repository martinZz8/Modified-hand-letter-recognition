import sys
from os.path import dirname

sys.path.append(dirname(dirname(dirname(__file__))))
from consts.consts import availableLetters


def mapRecognitionsToIndexes(recognitionResults: list):
    recognitionResultsIdx = [availableLetters.index(letter) for letter in recognitionResults]

    return recognitionResultsIdx
