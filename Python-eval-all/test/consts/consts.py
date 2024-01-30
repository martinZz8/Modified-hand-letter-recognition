# When invoking "main-test.py" script, use parameters such as:
# 1) -m, --media-pipe OR -o, --open-pose (IMPORTANT)
# 2) -p, --preprocessing OR -P, --no-preprocessing
# 3) -s, --shifted-data OR -S, --no-shifted-data
# 4) -r, --image-resize OR -R, --skeleton-rescale
# 5*) -f, --input-folder-path (IMPORTANT)
# 6*) -C, --cpu (use that option, since is faster than -c, --cuda)

# This makes 12 (2*3*2) combinations available to test:
# with -m OR -o (2),
# with -p (only with -s - this option doesn't matter here) OR -P (with -s OR -S) (3),
# with -r OR -R (2)

combinedOptions = [
    # model v1
    ["-m", "-p", "-s", "-r", "-v 2"],  # 0 - index
    ["-m", "-p", "-s", "-R", "-v 2"],  # 1
    ["-m", "-P", "-s", "-r", "-v 2"],  # 2
    ["-m", "-P", "-s", "-R", "-v 2"],  # 3
    ["-m", "-P", "-S", "-r", "-v 2"],  # 4
    ["-m", "-P", "-S", "-R", "-v 2"],  # 5
    ["-o", "-p", "-s", "-r", "-v 2"],  # 6
    ["-o", "-p", "-s", "-R", "-v 2"],  # 7
    ["-o", "-P", "-s", "-r", "-v 2"],  # 8
    ["-o", "-P", "-s", "-R", "-v 2"],  # 9
    ["-o", "-P", "-S", "-r", "-v 2"],  # 10
    ["-o", "-P", "-S", "-R", "-v 2"],  # 11
    # model v2
    ["-o", "-p", "-s", "-r", "-v 2"],  # 12
    ["-o", "-p", "-s", "-R", "-v 2"],  # 13
    ["-o", "-P", "-s", "-r", "-v 2"],  # 14
    ["-o", "-P", "-s", "-R", "-v 2"],  # 15
    ["-o", "-P", "-S", "-r", "-v 2"],  # 16
    ["-o", "-P", "-S", "-R", "-v 2"]   # 17
]

combinedOptionsLoso = [
    # Person 1
    ["-m", "-p", "-s", "-l 1", "-v 2"],
    ["-m", "-p", "-S", "-l 1", "-v 2"],
    ["-m", "-P", "-s", "-l 1", "-v 2"],
    ["-m", "-P", "-S", "-l 1", "-v 2"],
    # ...
    ["-o", "-p", "-s", "-l 1", "-v 2"],
    ["-o", "-p", "-S", "-l 1", "-v 2"],
    ["-o", "-P", "-s", "-l 1", "-v 2"],
    ["-o", "-P", "-S", "-l 1", "-v 2"],
    # Person 2
    ["-m", "-p", "-s", "-l 2", "-v 2"],
    ["-m", "-p", "-S", "-l 2", "-v 2"],
    ["-m", "-P", "-s", "-l 2", "-v 2"],
    ["-m", "-P", "-S", "-l 2", "-v 2"],
    # ...
    ["-o", "-p", "-s", "-l 2", "-v 2"],
    ["-o", "-p", "-S", "-l 2", "-v 2"],
    ["-o", "-P", "-s", "-l 2", "-v 2"],
    ["-o", "-P", "-S", "-l 2", "-v 2"],
    # Person 3
    ["-m", "-p", "-s", "-l 3", "-v 2"],
    ["-m", "-p", "-S", "-l 3", "-v 2"],
    ["-m", "-P", "-s", "-l 3", "-v 2"],
    ["-m", "-P", "-S", "-l 3", "-v 2"],
    # ...
    ["-o", "-p", "-s", "-l 3", "-v 2"],
    ["-o", "-p", "-S", "-l 3", "-v 2"],
    ["-o", "-P", "-s", "-l 3", "-v 2"],
    ["-o", "-P", "-S", "-l 3", "-v 2"],
    # Person 4
    ["-m", "-p", "-s", "-l 4", "-v 2"],
    ["-m", "-p", "-S", "-l 4", "-v 2"],
    ["-m", "-P", "-s", "-l 4", "-v 2"],
    ["-m", "-P", "-S", "-l 4", "-v 2"],
    # ...
    ["-o", "-p", "-s", "-l 4", "-v 2"],
    ["-o", "-p", "-S", "-l 4", "-v 2"],
    ["-o", "-P", "-s", "-l 4", "-v 2"],
    ["-o", "-P", "-S", "-l 4", "-v 2"],
    # Person 5
    ["-m", "-p", "-s", "-l 5", "-v 2"],
    ["-m", "-p", "-S", "-l 5", "-v 2"],
    ["-m", "-P", "-s", "-l 5", "-v 2"],
    ["-m", "-P", "-S", "-l 5", "-v 2"],
    # ...
    ["-o", "-p", "-s", "-l 5", "-v 2"],
    ["-o", "-p", "-S", "-l 5", "-v 2"],
    ["-o", "-P", "-s", "-l 5", "-v 2"],
    ["-o", "-P", "-S", "-l 5", "-v 2"],
    # Person 6
    ["-m", "-p", "-s", "-l 6", "-v 2"],
    ["-m", "-p", "-S", "-l 6", "-v 2"],
    ["-m", "-P", "-s", "-l 6", "-v 2"],
    ["-m", "-P", "-S", "-l 6", "-v 2"],
    # ...
    ["-o", "-p", "-s", "-l 6", "-v 2"],
    ["-o", "-p", "-S", "-l 6", "-v 2"],
    ["-o", "-P", "-s", "-l 6", "-v 2"],
    ["-o", "-P", "-S", "-l 6", "-v 2"],
    # Person 7
    ["-m", "-p", "-s", "-l 7", "-v 2"],
    ["-m", "-p", "-S", "-l 7", "-v 2"],
    ["-m", "-P", "-s", "-l 7", "-v 2"],
    ["-m", "-P", "-S", "-l 7", "-v 2"],
    # ...
    ["-o", "-p", "-s", "-l 7", "-v 2"],
    ["-o", "-p", "-S", "-l 7", "-v 2"],
    ["-o", "-P", "-s", "-l 7", "-v 2"],
    ["-o", "-P", "-S", "-l 7", "-v 2"],
    # Person 8
    ["-m", "-p", "-s", "-l 8", "-v 2"],
    ["-m", "-p", "-S", "-l 8", "-v 2"],
    ["-m", "-P", "-s", "-l 8", "-v 2"],
    ["-m", "-P", "-S", "-l 8", "-v 2"],
    # ...
    ["-o", "-p", "-s", "-l 8", "-v 2"],
    ["-o", "-p", "-S", "-l 8", "-v 2"],
    ["-o", "-P", "-s", "-l 8", "-v 2"],
    ["-o", "-P", "-S", "-l 8", "-v 2"],
    # Person 9
    ["-m", "-p", "-s", "-l 9", "-v 2"],
    ["-m", "-p", "-S", "-l 9", "-v 2"],
    ["-m", "-P", "-s", "-l 9", "-v 2"],
    ["-m", "-P", "-S", "-l 9", "-v 2"],
    # ...
    ["-o", "-p", "-s", "-l 9", "-v 2"],
    ["-o", "-p", "-S", "-l 9", "-v 2"],
    ["-o", "-P", "-s", "-l 9", "-v 2"],
    ["-o", "-P", "-S", "-l 9", "-v 2"],
    # Person 10
    ["-m", "-p", "-s", "-l 10", "-v 2"],
    ["-m", "-p", "-S", "-l 10", "-v 2"],
    ["-m", "-P", "-s", "-l 10", "-v 2"],
    ["-m", "-P", "-S", "-l 10", "-v 2"],
    # ...
    ["-o", "-p", "-s", "-l 10", "-v 2"],
    ["-o", "-p", "-S", "-l 10", "-v 2"],
    ["-o", "-P", "-s", "-l 10", "-v 2"],
    ["-o", "-P", "-S", "-l 10", "-v 2"],
    # Person 11
    ["-m", "-p", "-s", "-l 11", "-v 2"],
    ["-m", "-p", "-S", "-l 11", "-v 2"],
    ["-m", "-P", "-s", "-l 11", "-v 2"],
    ["-m", "-P", "-S", "-l 11", "-v 2"],
    # ...
    ["-o", "-p", "-s", "-l 11", "-v 2"],
    ["-o", "-p", "-S", "-l 11", "-v 2"],
    ["-o", "-P", "-s", "-l 11", "-v 2"],
    ["-o", "-P", "-S", "-l 11", "-v 2"],
    # ...
    # Person 12
    ["-m", "-p", "-s", "-l 12", "-v 2"],
    ["-m", "-p", "-S", "-l 12", "-v 2"],
    ["-m", "-P", "-s", "-l 12", "-v 2"],
    ["-m", "-P", "-S", "-l 12", "-v 2"],
    # ...
    ["-o", "-p", "-s", "-l 12", "-v 2"],
    ["-o", "-p", "-S", "-l 12", "-v 2"],
    ["-o", "-P", "-s", "-l 12", "-v 2"],
    ["-o", "-P", "-S", "-l 12", "-v 2"]
]

availableLetters: list[str] = ['A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'L', 'M', 'N', 'O', 'P', 'R', 'W', 'Y']
