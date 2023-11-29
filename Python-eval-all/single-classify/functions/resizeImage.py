# Standard imports
import cv2


def printImageShapes(image, title):
    imageHeight, imageWidth, imageChannels = image.shape

    print(f"{title}:\n"
          f"- imageWidth: {imageWidth}px,\n"
          f"- imageHeight: {imageHeight}px,\n"
          f"- imageChannels: {imageChannels}")


def resizeImage(inputImageFilePath: str,
                outputImageFilePath: str,
                desiredImageWidth: int,
                desiredImageHeight: int,
                useCubicInterpolation: bool = False):
    # Read image located in "inputImageFilePath" to get current image width and height
    image = cv2.imread(inputImageFilePath)
    printImageShapes(image, "Input image shapes")

    # If current shape doesn't match desired shape, perform rescaling skeletons
    imageHeight, imageWidth, imageChannels = image.shape

    if imageWidth != desiredImageWidth or imageHeight != desiredImageHeight:
        print(f"Performing resize, since shape doesn't match desired one")

        interpolationType = cv2.INTER_LINEAR
        if useCubicInterpolation:
            interpolationType = cv2.INTER_CUBIC

        resizedImage = cv2.resize(image, (desiredImageWidth, desiredImageHeight), interpolation=interpolationType)
        printImageShapes(resizedImage, "Resized image shapes")

        # Save "resizedImage" to "outputImageFilePath"
        cv2.imwrite(outputImageFilePath, resizedImage)
        print(f"outputImageFilePath: {outputImageFilePath}")
        return True
    else:
        print(f"Skipping resizing, since shape matches desired one")
        return False
