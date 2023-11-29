import getopt
import sys


def getArgumentOptionsSingle(argv,
                             useMediaPipe: bool,
                             useMatlabPreprocessing: bool,
                             useShiftedData: bool,
                             inputFolderPath: str,
                             inputImageName: str,
                             useImageResize: bool,
                             useCuda: bool):
    # --Read input arguments and set variables--
    # Note:
    # - each option consists of key and value pair
    # - to use short option, write hyphen followed by letter (and then space and value), e.g. "-i info.txt"
    # - to use long option, write double hyphen followed by string (and then space and value), e.g. "--long-option info.txt"

    # Also note, that in second argument of "getopt.getopt()" method (short args) you should provice colon ':' after short argument, if it's with value, otherwise no.
    # Same thing goes to third argument (long args), but with equal sign '='.
    opts, args = getopt.getopt(argv, "hmopPsSf:i:rRcC",
                               ["help", "media-pipe", "open-pose", "preprocessing", "no-preprocessing", "shifted-data", "no-shifted-data", "input-folder-path=", "input-image=", "image-resize", "skeleton-rescale", "cuda", "cpu"])

    for opt, arg in opts:
        if opt in ("-h", "--help"):  # help
            print('Available options:\n'
                  '-h, --help (help)\n'
                  '-m, --media-pipe (use MediaPipe - default)\n'
                  '-o, --open-pose (use OpenPose)\n'
                  '-p, --preprocessing (use Matlab preprocessing, skeleton transformation script - default)\n'
                  '-P, --no-preprocessing (do not use Matlab preprocessing, skeleton transformation script)\n'
                  '-s, --shifted-data (use shifted data - default)\n'
                  '-S, --no-shifted-data (use non-shifted data)\n'
                  '-f, --input-folder-path (specify input folder path - default "")\n'
                  '-i, --input-image (specify input image file name - default "P2_A.bmp")\n'
                  '-r, --image-resize (use image resize)\n'
                  '-R, --skeleton-rescale (use skeleton rescale - default)\n'
                  '-c, --cuda (use cuda if available - default)\n'
                  '-C, --cpu (use cpu)\n\n'
                  'Also note, that you should use only one of the following pair values (otherwise it would be used the least provided):\n'
                  '-m, -o\n'
                  '-p, -P\n'
                  '-s, -S\n'
                  '-r, -R\n'
                  '-c, -C')
            sys.exit()
        elif opt in ("-m", "--media-pipe"):  # use MediaPipe data - default
            useMediaPipe = True
        elif opt in ("-o", "--open-pose"):  # use OpenPose data
            useMediaPipe = False
        elif opt in ("-p", "--preprocessing"):  # use Matlab preprocessing, skeleton transformation script - default
            useMatlabPreprocessing = True
        elif opt in ("-P", "--no-preprocessing"):  # do not use Matlab preprocessing, skeleton transformation script
            useMatlabPreprocessing = False
        elif opt in ("-s", "--shifted-data"):  # use shifted data - default
            useShiftedData = True
        elif opt in ("-S", "--no-shifted-data"):  # use non-shifted data
            useShiftedData = False
        elif opt in ("-f", "--input-folder-path"):  # (specify input folder path - default "")
            inputFolderPath = arg
        elif opt in ("-i", "--input-image"):  # (specify input image file name - default "P2_A.bmp")
            inputImageName = arg
        elif opt in ("-r", "--image-resize"):  # (use image resize)
            useImageResize = True
        elif opt in ("-R", "--skeleton-rescale"):  # (use skeleton rescale - default)
            useImageResize = False
        elif opt in ("-c", "--cuda"):  # use cuda if available - default
            useCuda = True
        elif opt in ("-C", "--cpu"):  # use cpu
            useCuda = False

    # *Swap "useShiftedData" to False, when "useMatlabPreprocessing" is False - shifting cannot be performed when preprocessing isn't performed
    # if not useMatlabPreprocessing:
    #     useShiftedData = False

    print(f"Used options:\n"
          f"- useMediaPipe = {useMediaPipe}\n"
          f"- useMatlabPreprocessing = {useMatlabPreprocessing}\n"
          f"- useShiftedData = {useShiftedData}\n"
          f"- inputFolderPath = {inputFolderPath}\n"
          f"- inputImageName = {inputImageName}\n"
          f"- useImageResize = {useImageResize}\n"
          f"- useCuda = {useCuda}\n")

    return useMediaPipe, useMatlabPreprocessing, useShiftedData, inputFolderPath, inputImageName, useImageResize, useCuda
