-- IMPORTANT NOTES --
1) Input skeleton should not be shifted,
2) It will be shifted inside the script,
3) If it's shifted, it wouldn't be a big problem

-- DO BEFORE RUN (in order) --
1) paste tested skeleton into "input" folder (can be many files in here),
2) run matlab script passing input parameters (specified below in section "AVAILABLE PARAMETERS")

-- AVAILABLE PARAMETERS --
1) inputFileName (string - default "P2_A_M.txt") - name of the input file placed in "input" folder,
2) useMediaPipe (string "true", 1 or "false", 0 - default true) - determines whether to use MediaPipe data or not,
3) useShiftedOut (string "true", 1 or "false", 0 - default true) - determines if saved skeleton will be shifted or not (but always will be transformed using counted parameters from evolutional algorithm)

-- WAYS OF RUNNING SCRIPT --
(Note! you have to be in folder, where script exists or use relative path to it):
1 - **obsolete**)
matlab -nodisplay -nosplash -nodesktop -r "run('main.m'); exit;"

1.1 - with input parameter **obsolete**)
matlab -nodisplay -nosplash -nodesktop -r "inputFileName='P2_A_M.txt'; useMediaPipe='true'; useShiftedOut='true'; run('main.m'); exit;"

2)
matlab -batch "run('main.m'); exit;"

2.1 - with input parameter **RECOMMENDED**)
matlab -batch "inputFileName='P2_A_M.txt'; useMediaPipe='true'; useShiftedOut='true'; run('main.m'); exit;"

-- RESULT OF SCRIPT --
After termination of script, in "output" folder will appear 2 files:
- "ClassifiedLetter.txt" - contains in rows:
	- 1st: classified letter (as uppercase character),
	- 2nd: optimization function arguments (translateX, translateY, rotateZ (degrees), scaleX, scaleY),
	- 3rd: input file name,
	- 4rd: used dataset: MediaPipe or OpenPose,
	- 5th: is output skeleton shifted: True of False
- "TransformedSkeleton.txt" - contains input skeleton, that was transformed using counted parameters (rotation, translation, scaling) and could be shifted (if "useShiftedOut" parameter is default or set to "true" or 1)
