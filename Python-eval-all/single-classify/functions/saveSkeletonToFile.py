# Transform 2D array of "rescaledSkeleton" into proper str
def convert2DFloatSkeletonIntoStr(skeleton: list):
    joinedSkeletonStr = ""

    for idx1, row in enumerate(skeleton):
        for idx2, col in enumerate(row):
            joinedSkeletonStr += str(col)

            if idx2 != (len(row) - 1):
                joinedSkeletonStr += " "
        if idx1 != (len(skeleton) - 1):
            joinedSkeletonStr += "\n"

    return joinedSkeletonStr


# Save skeleton to file
def saveSkeletonToFile(skeletonFilePath: str, skeleton: list):
    joinedSkeletonStr = convert2DFloatSkeletonIntoStr(skeleton)

    with open(skeletonFilePath, "w") as file:
        file.write(joinedSkeletonStr)
