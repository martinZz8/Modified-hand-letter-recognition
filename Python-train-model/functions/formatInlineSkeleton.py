def formatInlineSkeleton(inlineSkeleton: str) -> list:
    skeletonLines = list(
        filter(
            lambda x: len(x) > 0,
            inlineSkeleton.split("\n")
        )
    )  # Note! Here we remove blank lines by filtering them out

    skeletonLinesSplitted = list(
        map(
            lambda x: list(
                map(
                    lambda y: float(y),
                    x.split(" ")
                )
            ),
            skeletonLines
        )
    )

    return skeletonLinesSplitted
