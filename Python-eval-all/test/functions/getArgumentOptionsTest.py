import getopt
import sys

# When invoking "main-test.py" script, use parameters such as:
# 1) -m, --media-pipe OR -o, --open-pose (IMPORTANT)
# 2) -p, --preprocessing OR -P, --no-preprocessing
# 3) -s, --shifted-data OR -S, --no-shifted-data
# 4) -r, --image-resize OR -R, --skeleton-rescale
# 5*) -L, --standard-test (we don't use LOSO test)
# 6*) -f, --input-folder-path (IMPORTANT)
# 7*) -C, --cpu (use that option, since is faster than -c, --cuda)


def getArgumentOptionsTest(argv,
                           inputSingleFolderPath,
                           isLosoTest,
                           useCuda):
    # --Read input arguments and set variables--
    # Note:
    # - each option consists of key and value pair
    # - to use short option, write hyphen followed by letter (and then space and value), e.g. "-i info.txt"
    # - to use long option, write double hyphen followed by string (and then space and value), e.g. "--long-option info.txt"

    # Also note, that in second argument of "getopt.getopt()" method (short args) you should provice colon ':' after short argument, if it's with value, otherwise no.
    # Same thing goes to third argument (long args), but with equal sign '='.

    opts, args = getopt.getopt(argv, "hf:cClL",
                               ["help", "input-folder-path=", "cuda", "cpu", "loso-test", "standard-test"])

    for opt, arg in opts:
        if opt in ("-h", "--help"):  # help
            print('Available options:\n'
                  '-h, --help (help)\n'
                  '-f, --input-folder-path (specify input folder path - default "<curr_workdir_path>/input/images")\n'
                  '-l, --loso-test (specify, if we perform LOSO test)\n'
                  '-L, --standard-test (specify, if we perform standard test - default)\n'
                  '-c, --cuda (use cuda if available)\n'
                  '-C, --cpu (use cpu - default)\n\n'
                  'Also note, that you should use only one of the following pair values (otherwise it would be used the least provided):\n'
                  '-c, -C')
            sys.exit()
        elif opt in ("-f", "--input-folder-path"):  # specify input folder path - default "<curr_workdir_path>/input/images"
            inputSingleFolderPath = arg
        elif opt in ("-l", "--loso-test"):  # specify, if we perform LOSO test
            isLosoTest = True
        elif opt in ("-L", "--standard-test"):  # specify, if we perform standard test - default
            isLosoTest = False
        elif opt in ("-c", "--cuda"):  # use cuda if available - default
            useCuda = True
        elif opt in ("-C", "--cpu"):  # use cpu
            useCuda = False

    print(f"Used options:\n"
          f"- inputSingleFolderPath = {inputSingleFolderPath}\n"
          f"- isLosoTest = {isLosoTest}\n"
          f"- useCuda = {useCuda}\n")

    return inputSingleFolderPath, isLosoTest, useCuda
