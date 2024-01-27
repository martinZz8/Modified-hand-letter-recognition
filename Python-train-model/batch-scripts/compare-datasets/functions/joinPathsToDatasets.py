from os.path import join


def joinPathsToDatasets(pathToDatasetsFolder: str,
                        useShiftedDataset: bool,
                        useMediaPipe: bool,
                        firstDatasetVersion: int,
                        secondDatasetVersion: int):
    # Check if we use shifted dataset
    if useShiftedDataset:
        # Prepare base path for "shifted" dataset
        pathToShiftedDatasetFolder = join(pathToDatasetsFolder, "shifted")

        pathToFirstComparedDataset = pathToShiftedDatasetFolder
        pathToSecondComparedDataset = pathToShiftedDatasetFolder
    else:
        # Prepare base path for "normal" dataset
        pathToNormalDatasetFolder = join(pathToDatasetsFolder, "normal")

        pathToFirstComparedDataset = pathToNormalDatasetFolder
        pathToSecondComparedDataset = pathToNormalDatasetFolder

    # Check if we use MediaPipe
    if useMediaPipe:
        pathToFirstComparedDataset = join(pathToFirstComparedDataset, "MediaPipe")
        pathToSecondComparedDataset = join(pathToSecondComparedDataset, "MediaPipe")
    else:
        pathToFirstComparedDataset = join(pathToFirstComparedDataset, "OpenPose")
        pathToSecondComparedDataset = join(pathToSecondComparedDataset, "OpenPose")

    # Check for version of dataset
    if firstDatasetVersion != 1:
        pathToFirstComparedDataset += str(firstDatasetVersion)

    if secondDatasetVersion != 1:
        pathToSecondComparedDataset += str(secondDatasetVersion)

    print(f"Path to first compared dataset: {pathToFirstComparedDataset}")
    print(f"Path to second compared dataset: {pathToSecondComparedDataset}")

    return pathToFirstComparedDataset, pathToSecondComparedDataset
