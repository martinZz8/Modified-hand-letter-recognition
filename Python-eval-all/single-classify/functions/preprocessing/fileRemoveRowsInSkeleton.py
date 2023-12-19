import sys
from os.path import dirname

sys.path.append(dirname(dirname(__file__)))
from readSkeletonFromFile import readSkeletonFromFile
from saveSkeletonToFile import saveSkeletonToFile


def fileRemoveRowsInSkeleton(skeletonPath: str, removeAllRowsToProperSize: bool = False, numOfElementsToMaintain: int = 21):
    # Read skeleton from file
    skeleton = readSkeletonFromFile(skeletonPath)

    # Perform removal of last row
    if not removeAllRowsToProperSize:
        skeleton = skeleton[0:len(skeleton) - 1]
    else:
        skeleton = skeleton[0:numOfElementsToMaintain]

    # Save skeleton to file
    saveSkeletonToFile(skeletonPath, skeleton)
