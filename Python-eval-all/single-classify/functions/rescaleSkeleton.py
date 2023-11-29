# Standard imports
import cv2

# Custom functions imports
from normalizeValues import normalizeValuesOwnRowCol
from readSkeletonFromFile import readSkeletonFromFile
from saveSkeletonToFile import saveSkeletonToFile


# Additional info: how to get RGB or BGR values from every pixel in image loaded by OpenCV (in height,width,channel manner) or PIL (in width, height manner) libraries:
# https://stackoverflow.com/questions/57252787/is-there-a-way-to-get-a-pixels-color-value-and-store-the-value-in-a-txt-file
def rescaleSkeleton(inputImageFilePath: str,
                    skeletonFilePath: str,
                    desiredImageWidth: int,
                    desiredImageHeight: int):
    # Read image located in "inputImageFilePath" to get current image width and height
    image = cv2.imread(inputImageFilePath)
    imageHeight, imageWidth, imageChannels = image.shape
    print(f"Input image shapes:\n"
          f"- imageWidth: {imageWidth}px,\n"
          f"- imageHeight: {imageHeight}px,\n"
          f"- imageChannels: {imageChannels}")

    # If current shape doesn't match desired shape, perform rescaling skeletons
    if imageWidth != desiredImageWidth or imageHeight != desiredImageHeight:
        print(f"Performing rescale, since shape doesn't match desired one")
        # Read skeleton located in "skeletonFilePath" folder
        loadedSkeleton = readSkeletonFromFile(skeletonFilePath)

        # Rescale skeleton
        rescaledSkeleton = normalizeValuesOwnRowCol(loadedSkeleton,
                                                    0,
                                                    desiredImageWidth,
                                                    0,
                                                    desiredImageHeight,
                                                    0,
                                                    imageWidth,
                                                    0,
                                                    imageHeight,
                                                    isInt=False,
                                                    usetwoDecimalPoints = True)

        # Transform 2D array of "rescaledSkeleton" into proper str and save it to file
        saveSkeletonToFile(skeletonFilePath, rescaledSkeleton)
        return True
    else:
        print(f"Skipping rescaling, since shape matches desired one")
        return False
