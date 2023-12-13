import getopt
import sys


def getArgumentOptionsBatch(argv,
                            resultFileName):
    # --Read input arguments and set variables--
    # Note:
    # - each option consists of key and value pair
    # - to use short option, write hyphen followed by letter (and then space and value), e.g. "-i info.txt"
    # - to use long option, write double hyphen followed by string (and then space and value), e.g. "--long-option info.txt"

    # Also note, that in second argument of "getopt.getopt()" method (short args) you should provice colon ':' after short argument, if it's with value, otherwise no.
    # Same thing goes to third argument (long args), but with equal sign '='.

    opts, args = getopt.getopt(argv, "hf:",
                               ["help", "input-file-name="])

    for opt, arg in opts:
        if opt in ("-h", "--help"):  # help
            print('Available options:\n'
                  '-h, --help (help)\n'
                  '-f, --input-file-name (specify input file name - default "results_1.txt")\n')
            sys.exit()
        elif opt in ("-f", "--input-file-name"):  # specify input file name - default "results_1.txt"
            resultFileName = arg

    print(f"Used options:\n"
          f"- resultFileName = {resultFileName}")

    return resultFileName

