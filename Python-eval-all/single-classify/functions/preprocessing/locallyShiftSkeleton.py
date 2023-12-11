# Standard imports
# import sys

# sys.path.append("../../functions")
from .. import readSkeletonFromFile
from .. import saveSkeletonToFile


def countSkeletonCoG(skeleton: list):
    cx, cy = (0, 0)

    for row in skeleton:
        cx += row[0]
        cy += row[1]

    cx /= len(skeleton)
    cy /= len(skeleton)

    return cx, cy


def locallyShiftSkeleton(skeletonPath: str,
                         useMediaPipe: bool):
    # Read skeleton from file
    skeleton = readSkeletonFromFile.readSkeletonFromFile(skeletonPath)

    # If OpenPose data, perform removal of last, redundant 22nd row
    if not useMediaPipe:
        skeleton = skeleton[0:len(skeleton) - 1]

    # Count skeleton's CoG
    cx, cy = countSkeletonCoG(skeleton)

    # Move skeleton, that his new CoG is in point (0, 0)
    for row in skeleton:
        row[0] = round(row[0] - cx, 2)
        row[1] = round(row[1] - cy, 2)

    # Save skeleton to file
    saveSkeletonToFile.saveSkeletonToFile(skeletonPath, skeleton)

    return skeleton
