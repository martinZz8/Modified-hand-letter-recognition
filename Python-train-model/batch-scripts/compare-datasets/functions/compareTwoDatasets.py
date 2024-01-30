import sys
from os import listdir
from os.path import dirname, join, isdir, isfile

sys.path.append(dirname(__file__))
from loadSkeleton import loadSkeleton


def compareTwoDatasets(pathToFirstDataset: str,
                       pathToSecondDataset: str):
    # --Initialize aggregated values--
    resultStr = f"Path to first compared dataset: {pathToFirstDataset}\n" \
                f"Path to second compared dataset: {pathToSecondDataset}\n\n"

    # --Determine letters of MediaPipe and OpenPose folders--
    fLetters = set([f for f in listdir(pathToFirstDataset) if isdir(join(pathToFirstDataset, f))])
    sLetters = set([f for f in listdir(pathToSecondDataset) if isdir(join(pathToSecondDataset, f))])

    if fLetters != sLetters:
        raise Exception("Error: letters in first path doesn't match letters in second path")

    # --Compare corresponding point clouds from each letter from first and second datasets--
    allNotEqualRows = []
    for letter in fLetters:
        fPath = join(pathToFirstDataset, letter)
        sPath = join(pathToSecondDataset, letter)

        # --Determine letters of MediaPipe and OpenPose folders--
        fPointClouds = set([f for f in listdir(fPath) if isfile(join(fPath, f))])
        sPointClouds = set([f for f in listdir(sPath) if isfile(join(sPath, f))])
        intersectedPointClouds = fPointClouds.intersection(sPointClouds)

        if len(intersectedPointClouds) == 0:
            raise Exception(f"Error: intersection of point clouds in path '{fPath}' and '{sPath}' is blank")

        for pointCloudName in intersectedPointClouds:
            fPointCloudName = join(fPath, pointCloudName)
            sPointCloudName = join(sPath, pointCloudName)

            # --Compare first and second point clouds--
            fPointCloud = loadSkeleton(fPointCloudName)
            sPointCloud = loadSkeleton(sPointCloudName)

            if len(fPointCloud) != len(sPointCloud):
                raise Exception("Error: length of first point cloud doesn't match length of second one")

            notEqualElements = []
            for i in range(len(fPointCloud)):
                fRow = fPointCloud[i]
                sRow = sPointCloud[i]

                for j in range(len(fRow)):
                    if fRow[j] != sRow[j]:
                        notEqualElements.append({
                            "pointCloudFileName": pointCloudName,
                            "rowIdx": i,
                            "columnIdx": j,
                            "firstElement": fRow[j],
                            "secondElement": sRow[j],
                            "absoluteDifference": abs(fRow[j] - sRow[j])
                        })

            if len(notEqualElements) > 0:
                allNotEqualRows.append({
                    "letter": letter,
                    "notEqualElements": notEqualElements
                })

        # --If compared point clouds aren't equal ('notEqualRows' isn't empty), log it into file
        if len(allNotEqualRows) > 0:
            for idx, item in enumerate(allNotEqualRows):
                resultStr += f"--Letter '{item['letter']}'--\n"

                for idx2, item2 in enumerate(item["notEqualElements"]):
                    resultStr += f"{idx2+1})\n" \
                                 f"point cloud file name: {item2['pointCloudFileName']}\n" \
                                 f"rowIdx: {item2['rowIdx']}\n" \
                                 f"columnIdx: {item2['columnIdx']}\n" \
                                 f"firsElement: {item2['firstElement']}\n" \
                                 f"secondElement: {item2['secondElement']}\n" \
                                 f"absoluteDifference: {item2['absoluteDifference']}"

                    if idx2 != (len(item["notEqualElements"]) - 1):
                        resultStr += "\n"

                if idx != (len(allNotEqualRows) - 1):
                    resultStr += "\n\n"

    return resultStr
