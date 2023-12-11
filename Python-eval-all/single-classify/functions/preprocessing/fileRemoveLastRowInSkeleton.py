from .. import readSkeletonFromFile
from .. import saveSkeletonToFile


def fileRemoveLastRowInSkeleton(skeletonPath: str):
    # Read skeleton from file
    skeleton = readSkeletonFromFile.readSkeletonFromFile(skeletonPath)

    # Perform removal of last row
    skeleton = skeleton[0:len(skeleton) - 1]

    # Save skeleton to file
    saveSkeletonToFile.saveSkeletonToFile(skeletonPath, skeleton)
