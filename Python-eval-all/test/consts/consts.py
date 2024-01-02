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
    ["-m", "-p", "-s", "-r", "-v 1"],  # 0 - index
    ["-m", "-p", "-s", "-R", "-v 1"],  # 1
    ["-m", "-P", "-s", "-r", "-v 1"],  # 2
    ["-m", "-P", "-s", "-R", "-v 1"],  # 3
    ["-m", "-P", "-S", "-r", "-v 1"],  # 4
    ["-m", "-P", "-S", "-R", "-v 1"],  # 5
    ["-o", "-p", "-s", "-r", "-v 1"],  # 6
    ["-o", "-p", "-s", "-R", "-v 1"],  # 7
    ["-o", "-P", "-s", "-r", "-v 1"],  # 8
    ["-o", "-P", "-s", "-R", "-v 1"],  # 9
    ["-o", "-P", "-S", "-r", "-v 1"],  # 10
    ["-o", "-P", "-S", "-R", "-v 1"],   # 11
    # model v2
    ["-o", "-p", "-s", "-r", "-v 2"],  # 12
    ["-o", "-p", "-s", "-R", "-v 2"],  # 13
    ["-o", "-P", "-s", "-r", "-v 2"],  # 14
    ["-o", "-P", "-s", "-R", "-v 2"],  # 15
    ["-o", "-P", "-S", "-r", "-v 2"],  # 16
    ["-o", "-P", "-S", "-R", "-v 2"]  # 17
]

availableLetters: list[str] = ['A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'L', 'M', 'N', 'O', 'P', 'R', 'W', 'Y']
