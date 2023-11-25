import getopt
import sys


def getArgumentOptions(argv,
                       useMediaPipe: bool,
                       useShiftedData: bool,
                       useCuda: bool,
                       modelRepeats: int):
    # --Read input arguments and set variables--
    # Note:
    # - each option consists of key and value pair
    # - to use short option, write hyphen followed by letter (and then space and value), e.g. "-i info.txt"
    # - to use long option, write double hyphen followed by string (and then space and value), e.g. "--long-option info.txt"

    # Also note, that in second argument of "getopt.getopt()" method (short args) you should provice colon ':' after short argument, if it's with value, otherwise no.
    # Same thing goes to third argument (long args), but with equal sign '='.
    opts, args = getopt.getopt(argv, "hmosScCr:",
                               ["help", "media-pipe", "open-pose", "shifted-data", "no-shifted-data", "cuda", "cpu",
                                "model-repeats="])

    for opt, arg in opts:
        if opt in ("-h", "--help"):  # help
            print('Available options:\n'
                  '-h, --help (help)\n'
                  '-m, --media-pipe (use MediaPipe - default)\n'
                  '-o, --open-pose (use OpenPose)\n'
                  '-s, --shifted-data (use shifted data - default)\n'
                  '-S, --no-shifted-data (use non-shifted data)\n'
                  '-c, --cuda (use cuda if available - default)\n'
                  '-C, --cpu (use cpu)'
                  '-r, --model-repeats (number of model repeats, gets only best model based in train and test acc - default 1)\n\n'
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
        elif opt in ("-c", "--cuda"):  # use cuda if available - default
            useCuda = True
        elif opt in ("-C", "--cpu"):  # use cpu
            useCuda = False
        elif opt in ("-r", "--model-repeats"):  # set modelRepeats value - default 1
            # Check if "arg" string has integer representation of value (that could be casted to int)
            if arg.isnumeric():
                modelRepeats = int(arg)
            else:
                raise Exception("'-r' or '--model-repeats' parameter can have argument only of type integer")

    print(f"Used options:\n"
          f"- useMediaPipe = {useMediaPipe}\n"
          f"- useShiftedData = {useShiftedData}\n"
          f"- useCuda = {useCuda}\n"
          f"- modelRepeats = {modelRepeats}")

    return useMediaPipe, useShiftedData, useCuda, modelRepeats
