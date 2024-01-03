import getopt
import sys


def getBatchCompareArgumentOptions(argv,
                                   useMediaPipe: bool,
                                   useShiftedDataset: bool,
                                   firstDatasetVersion: int,
                                   secondDatasetVersion: int,
                                   outputFileName: str):
    # --Read input arguments and set variables--
    # Note:
    # - each option consists of key and value pair
    # - to use short option, write hyphen followed by letter (and then space and value), e.g. "-i info.txt"
    # - to use long option, write double hyphen followed by string (and then space and value), e.g. "--long-option info.txt"

    # Also note, that in second argument of "getopt.getopt()" method (short args) you should provice colon ':' after short argument, if it's with value, otherwise no.
    # Same thing goes to third argument (long args), but with equal sign '='.
    opts, args = getopt.getopt(argv, "hmosSf:d:u:",
                               ["help", "media-pipe", "open-pose", "shifted-dataset", "normal-dataset", "first-dataset-version=", "second-dataset-version=", "output-file-name="])

    for opt, arg in opts:
        if opt in ("-h", "--help"):  # help
            print('Available options:\n'
                  '-h, --help (help)\n'
                  '-m, --media-pipe (use MediaPipe - default)\n'
                  '-o, --open-pose (use OpenPose)\n'
                  '-s, --shifted-dataset (use shifted dataset - default)\n'
                  '-S, --normal-dataset (use non-shifted dataset)\n'
                  '-f, --first-dataset-version (specify first dataset version - default 1)\n'
                  '-d, --second-dataset-version (specify second dataset version - default 2)\n'
                  '-u, --output-file-name (specify output file name - default "", stands for "results.txt")\n\n'
                  'Also note, that you should use only one of the following pair values (otherwise it would be used the least provided):\n'
                  '-m, -o\n'
                  '-s, -S')
            sys.exit()
        elif opt in ("-m", "--media-pipe"):  # use MediaPipe
            useMediaPipe = True
        elif opt in ("-o", "--open-pose"):  # use OpenPose - default
            useMediaPipe = False
        elif opt in ("-s", "--shifted-dataset"):  # use shifted dataset - default
            shiftedDataset = True
        elif opt in ("-S", "--normal-dataset"):  # use non-shifted dataset
            shiftedDataset = False
        elif opt in ("-f", "--first-dataset-version"):  # specify first dataset version - default 1
            # Check if "arg" string has integer representation of value (that could be casted to int)
            if arg.isnumeric():
                firstDatasetVersion = int(arg)
        elif opt in ("-d", "--second-dataset-version"):  # specify second dataset version - default 2
            # Check if "arg" string has integer representation of value (that could be casted to int)
            if arg.isnumeric():
                secondDatasetVersion = int(arg)
        elif opt in ("-u", "--output-file-name"):  # specify output file name - default "results.txt"
            outputFileName = arg

    print(f"Used options:\n"
          f"- useMediaPipe = {useMediaPipe}\n"
          f"- useShiftedDataset = {useShiftedDataset}\n"
          f"- firstDatasetVersion = {firstDatasetVersion}\n"
          f"- secondDatasetVersion = {secondDatasetVersion}\n"
          f"- outputFileName = {outputFileName}\n")

    return useMediaPipe, useShiftedDataset, firstDatasetVersion, secondDatasetVersion, outputFileName
