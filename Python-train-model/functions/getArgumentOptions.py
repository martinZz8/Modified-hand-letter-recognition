import getopt
import sys


# Custom exception declarations (only used and caught in this file)
class WrongLOSOPersonInteger(Exception):
    pass


class WrongDatasetVersionInteger(Exception):
    pass


def getArgumentOptions(argv,
                       useMediaPipe: bool,
                       versionOfDataset: int,
                       useShiftedData: bool,
                       losoPersonTester: int,
                       useCuda: bool,
                       modelRepeats: int,
                       showGraphs: bool):
    # --Read input arguments and set variables--
    # Note:
    # - each option consists of key and value pair
    # - to use short option, write hyphen followed by letter (and then space and value), e.g. "-i info.txt"
    # - to use long option, write double hyphen followed by string (and then space and value), e.g. "--long-option info.txt"

    # Also note, that in second argument of "getopt.getopt()" method (short args) you should provice colon ':' after short argument, if it's with value, otherwise no.
    # Same thing goes to third argument (long args), but with equal sign '='.
    opts, args = getopt.getopt(argv, "hmov:sSl:cCr:gG",
                               ["help", "media-pipe", "open-pose", "dataset-version=", "shifted-data", "no-shifted-data", "loso-person-tester=", "cuda", "cpu", "model-repeats=", "show-graphs", "hide-graphs"])

    for opt, arg in opts:
        if opt in ("-h", "--help"):  # help
            print('Available options:\n'
                  '-h, --help (help)\n'
                  '-m, --media-pipe (use MediaPipe - default)\n'
                  '-o, --open-pose (use OpenPose)\n'
                  '-v, --dataset-version (version of used dataset - default 1)\n'
                  '-s, --shifted-data (use shifted data - default)\n'
                  '-S, --no-shifted-data (use non-shifted data)\n'
                  '-l, --loso-person-tester (specify, which person has to be LOSO tester, other persons are used to train model - default -1, which stands for not using LOSO dataset)\n'
                  '-c, --cuda (use cuda if available - default)\n'
                  '-C, --cpu (use cpu)'
                  '-r, --model-repeats (number of model repeats, gets only best model based in train and test acc - default 1)\n'
                  '-g, --show-graphs (show best model loss and accuracy graphs at the end of model training - default)\n'
                  '-G, --hide-graphs (hide best model loss and accuracy graphs at the end of model training)\n\n'
                  'Also note, that you should use only one of the following pair values (otherwise it would be used the least provided):\n'
                  '-m, -o\n'
                  '-s, -S\n'
                  '-c, -C\n',
                  '-g, -G')
            sys.exit()
        elif opt in ("-m", "--media-pipe"):  # use MediaPipe data - default
            useMediaPipe = True
        elif opt in ("-o", "--open-pose"):  # use OpenPose data
            useMediaPipe = False
        elif opt in ("-v", "--dataset-version"):  # version of used dataset - default 1
            # Check if "arg" string has integer representation of value (that could be casted to int)
            doesThrowWrongNumberException = False
            try:
                if arg.isnumeric():
                    intArg = int(arg)
                    if intArg >= 1:
                        versionOfDataset = intArg
                    else:
                        doesThrowWrongNumberException = True
                else:
                    doesThrowWrongNumberException = True

                if doesThrowWrongNumberException:
                    raise WrongDatasetVersionInteger()
            except WrongDatasetVersionInteger:
                raise Exception("'-v' or '--dataset-version' parameter can have argument only of type integer (from 1 to infinity)")
        elif opt in ("-s", "--shifted-data"):  # use shifted data - default
            useShiftedData = True
        elif opt in ("-S", "--no-shifted-data"):  # use non-shifted data
            useShiftedData = False
        elif opt in ("-l", "--loso-person-tester"):  # specify, which person has to be LOSO tester, other persons are used to train model - default -1, which stands for not using LOSO dataset
            # Check if "arg" string has integer representation of value (that could be casted to int)
            doesThrowWrongNumberException = False
            try:
                if arg.isnumeric():
                    intArg = int(arg)
                    if intArg >= -1:
                        losoPersonTester = intArg
                    else:
                        doesThrowWrongNumberException = True
                else:
                    doesThrowWrongNumberException = True

                if doesThrowWrongNumberException:
                    raise WrongLOSOPersonInteger()
            except WrongLOSOPersonInteger:
                raise Exception("'-l' or '--loso-person-tester' parameter can have argument only of type integer (from -1 to infinity)")
        elif opt in ("-c", "--cuda"):  # use cuda if available - default
            useCuda = True
        elif opt in ("-C", "--show-graphs"):  # use cpu
            useCuda = False
        elif opt in ("-g", "--hide-graphs"):  # show best model loss and accuracy graphs at the end of model training - default
            showGraphs = True
        elif opt in ("-G", "--cpu"):  # hide best model loss and accuracy graphs at the end of model training
            showGraphs = False
        elif opt in ("-r", "--model-repeats"):  # set modelRepeats value - default 1
            # Check if "arg" string has integer representation of value (that could be casted to int)
            if arg.isnumeric():
                modelRepeats = int(arg)
            else:
                raise Exception("'-r' or '--model-repeats' parameter can have argument only of type integer")

    print(f"Used options:\n"
          f"- useMediaPipe = {useMediaPipe}\n"
          f"- versionOfDataset = {versionOfDataset}\n"
          f"- useShiftedData = {useShiftedData}\n"
          f"- losoPersonTester = {losoPersonTester}{'(don''t use LOSO)' if losoPersonTester <= -1 else ''}\n"
          f"- useCuda = {useCuda}\n"
          f"- modelRepeats = {modelRepeats}\n",
          f"- showGraphs = {showGraphs}\n")

    return useMediaPipe, versionOfDataset, useShiftedData, losoPersonTester, useCuda, modelRepeats, showGraphs
