def determineUsedDatasetVersion(skeletonReceiver: str,
                                mediaPipeDatasetVersion: int,
                                openPoseDatasetVersion: int):
    return mediaPipeDatasetVersion if skeletonReceiver == '-m' else openPoseDatasetVersion
