import getopt
import sys

# When invoking "main-test.py" script, use parameters such as:
# 1) -m, --media-pipe OR -o, --open-pose (IMPORTANT)
# 2) -p, --preprocessing OR -P, --no-preprocessing
# 3) -s, --shifted-data OR -S, --no-shifted-data
# 4) -r, --image-resize OR -R, --skeleton-rescale
# 5*) -f, --input-folder-path (IMPORTANT)
# 6*) -C, --cpu (use that option, since is faster than -c, --cuda)


def getArgumentOptionsTest(argv,
                           selectedOptionIdx,
                           inputSingleFolderPath,
                           useCuda):
    # --Read input arguments and set variables--
    # Note:
    # - each option consists of key and value pair
    # - to use short option, write hyphen followed by letter (and then space and value), e.g. "-i info.txt"
    # - to use long option, write double hyphen followed by string (and then space and value), e.g. "--long-option info.txt"

    # Also note, that in second argument of "getopt.getopt()" method (short args) you should provice colon ':' after short argument, if it's with value, otherwise no.
    # Same thing goes to third argument (long args), but with equal sign '='.

    opts, args = getopt.getopt(argv, "hs:f:cC",
                               ["help", "selected-option-idx=", "input-folder-path=", "cuda", "cpu"])

    for opt, arg in opts:
        if opt in ("-h", "--help"):  # help
            print('Available options:\n'
                  '-h, --help (help)\n'
                  '-s, --selected-option-idx (specify selected option from range <0,11>; see "consts.py" file for more details of selected option - default 0)\n'
                  '-f, --input-folder-path (specify input folder path - default "<curr_workdir_path>/input/images")\n'                  
                  '-c, --cuda (use cuda if available)\n'
                  '-C, --cpu (use cpu - default)\n\n'
                  'Also note, that you should use only one of the following pair values (otherwise it would be used the least provided):\n'
                  '-c, -C')
            sys.exit()
        elif opt in ("-s", "--selected-option-idx"):  # specify selected option from range <0,11>; see "consts.py" file for more details of selected option - default 0
            # Check if "arg" string has integer representation of value (that could be casted to int)
            if arg.isnumeric():
                selectedOptionIdx = int(arg)
            else:
                raise Exception("'-s' or '--selected-option-idx' parameter can have argument only of type integer")
        elif opt in ("-f", "--input-folder-path"):  # specify input folder path - default "<curr_workdir_path>/input/images"
            inputSingleFolderPath = arg
        elif opt in ("-c", "--cuda"):  # use cuda if available - default
            useCuda = True
        elif opt in ("-C", "--cpu"):  # use cpu
            useCuda = False

    print(f"Used options:\n"
          f"- selectedOptionIdx = {selectedOptionIdx}\n"
          f"- inputSingleFolderPath = {inputSingleFolderPath}\n"
          f"- useCuda = {useCuda}\n")

    return selectedOptionIdx, inputSingleFolderPath, useCuda