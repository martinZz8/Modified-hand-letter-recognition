def doesImageNameContainsSpecificPersonNum(imageName: str,
                                           personNum: int):
    splittedImageName = imageName.split("_")

    if len(splittedImageName) == 2:
        splittedImageName2 = splittedImageName[0].split("P")

        if len(splittedImageName2) == 2:
            imagePersonNumStr = splittedImageName2[1]

            if imagePersonNumStr.isnumeric():
                imagePersonNum = int(imagePersonNumStr)

                return imagePersonNum == personNum
    return False
