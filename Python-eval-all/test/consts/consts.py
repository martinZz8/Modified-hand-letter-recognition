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
    ["-m", "-p", "-s", "-r"],  # 0 - index
    ["-m", "-p", "-s", "-R"],  # 1
    ["-m", "-P", "-s", "-r"],  # 2
    ["-m", "-P", "-s", "-R"],  # 3
    ["-m", "-P", "-S", "-r"],  # 4
    ["-m", "-P", "-S", "-R"],  # 5
    ["-o", "-p", "-s", "-r"],  # 6
    ["-o", "-p", "-s", "-R"],  # 7
    ["-o", "-P", "-s", "-r"],  # 8
    ["-o", "-P", "-s", "-R"],  # 9
    ["-o", "-P", "-S", "-r"],  # 10
    ["-o", "-P", "-S", "-R"]   # 11
]

availableLetters: list[str] = ['A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'L', 'M', 'N', 'O', 'P', 'R', 'W', 'Y']
