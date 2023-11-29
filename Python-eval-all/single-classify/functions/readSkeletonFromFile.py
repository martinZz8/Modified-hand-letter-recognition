def readSkeletonFromFile(skeletonFilePath: str):
    loadedSkeleton = []

    with open(skeletonFilePath, "r") as file:
        fileContent = file.read().split("\n")

        for idx, line in enumerate(fileContent):
            loadedSkeleton.append([])
            lineElementsStr = line.split(" ")

            for singleLineElementStr in lineElementsStr:
                loadedSkeleton[idx].append(float(singleLineElementStr))

    return loadedSkeleton
