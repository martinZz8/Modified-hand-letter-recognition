import getopt
import sys


def getArgumentOptionsEval(argv,
                           useMediaPipe: bool,
                           useShiftedData: bool,
                           modelVersion: int,
                           modelClassName: str,
                           inputSkeletonFileName: str,
                           outputFileName: str,
                           useCuda: bool):
    # --Read input arguments and set variables--
    # Note:
    # - each option consists of key and value pair
    # - to use short option, write hyphen followed by letter (and then space and value), e.g. "-i info.txt"
    # - to use long option, write double hyphen followed by string (and then space and value), e.g. "--long-option info.txt"

    # Also note, that in second argument of "getopt.getopt()" method (short args) you should provice colon ':' after short argument, if it's with value, otherwise no.
    # Same thing goes to third argument (long args), but with equal sign '='.
    opts, args = getopt.getopt(argv, "hmosSv:n:i:u:cC",
                               ["help", "media-pipe", "open-pose", "shifted-data", "no-shifted-data", "model-version=", "model-class-name=", "input-skeleton=", "output-file=", "cuda", "cpu"])

    for opt, arg in opts:
        if opt in ("-h", "--help"):  # help
            print('Available options:\n'
                  '-h, --help (help)\n'
                  '-m, --media-pipe (use MediaPipe - default)\n'
                  '-o, --open-pose (use OpenPose)\n'
                  '-s, --shifted-data (use shifted data - default)\n'
                  '-S, --no-shifted-data (use non-shifted data)\n'
                  '-v, --model-version (specify model version - default 1)\n'
                  '-n, --model-class-name (specify model class name - available: "UniversalModelV1"; default "UniversalModelV1")\n'
                  '-i, --input-skeleton (specify input skeleton file name - default "inputSkeletonMS_A6.txt")\n'
                  '-u, --output-file (specify output file name - default "" stands for auto incremented file name)\n'
                  '-c, --cuda (use cuda if available - default)\n'
                  '-C, --cpu (use cpu)\n\n'
                  'Also note, that you should use only one of the following pair values (otherwise it would be used the least provided):\n'
                  '-m, -o\n'
                  '-s, -S\n'
                  '-c, -C')
            sys.exit()
        elif opt in ("-m", "--media-pipe"):  # use MediaPipe data - default
            useMediaPipe = True
        elif opt in ("-o", "--open-pose"):  # use OpenPose data
            useMediaPipe = False
        elif opt in ("-s", "--shifted-data"):  # use shifted data - default
            useShiftedData = True
        elif opt in ("-S", "--no-shifted-data"):  # use non-shifted data
            useShiftedData = False
        elif opt in ("-v", "--model-version"):  # specify model version - default 1
            # Check if "arg" string has integer representation of value (that could be casted to int)
            if arg.isnumeric():
                modelVersion = int(arg)
            else:
                raise Exception("'-v' or '--model-version' parameter can have argument only of type integer")
        elif opt in ("-n", "--model-class-name"):  # (specify model class name - default "UniversalModelV1")
            modelClassName = arg
        elif opt in ("-i", "--input-skeleton"):  # (specify input skeleton file name - default "inputSkeleton.txt")
            inputSkeletonFileName = arg
        elif opt in ("-u", "--output-file"):  # (specify output file name - default "" stands for auto incremented file name)
            outputFileName = arg
        elif opt in ("-c", "--cuda"):  # use cuda if available - default
            useCuda = True
        elif opt in ("-C", "--cpu"):  # use cpu
            useCuda = False

    print(f"Used options:\n"
          f"- useMediaPipe = {useMediaPipe}\n"
          f"- useShiftedData = {useShiftedData}\n"
          f"- modelVersion = {modelVersion}\n"
          f"- modelClassName = {modelClassName}\n"
          f"- inputSkeletonFileName = {inputSkeletonFileName}\n"
          f"- outputFileName = {outputFileName}\n"
          f"- useCuda = {useCuda}\n")

    return useMediaPipe, useShiftedData, modelVersion, modelClassName, inputSkeletonFileName, outputFileName, useCuda
