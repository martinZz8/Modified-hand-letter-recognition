from .. import readSkeletonFromFile
from .. import saveSkeletonToFile


def fileRemoveRowsInSkeleton(skeletonPath: str, removeAllRowsToProperSize: bool = False):
    # Read skeleton from file
    skeleton = readSkeletonFromFile.readSkeletonFromFile(skeletonPath)

    # Perform removal of last row
    if not removeAllRowsToProperSize:
        skeleton = skeleton[0:len(skeleton) - 1]
    else:
        skeleton = skeleton[0:21]

    # Save skeleton to file
    saveSkeletonToFile.saveSkeletonToFile(skeletonPath, skeleton)
