To run this program, paste tested skeleton into "input" folder (can be many files in here).
After that, run matlab script passing input parameter named "inputFileName" (default value is specified, but can not work when input file isn't in required folder) and "useMediaPipe" ("true", "false", true or false)

We can run script in following ways (Note! you have to be in folder, where script exists or use relative path to it):
1 - **obsolete**)
matlab -nodisplay -nosplash -nodesktop -r "run('main.m'); exit;"

1.1 - with input parameter **obsolete**)
matlab -nodisplay -nosplash -nodesktop -r "inputFileName='P2_A_M.txt'; useMediaPipe='true'; run('main.m'); exit;"

2)
matlab -batch "run('main.m'); exit;"

2.1 - with input parameter **RECOMMENDED**)
matlab -batch "inputFileName='P2_A_M.txt'; useMediaPipe='true'; run('main.m'); exit;"

After termination of script, in "output" folder will appear 2 files:
- "ClassifiedLetter.txt" - contains in rows:
	- 1st: classified letter (as uppercase character),
	- 2nd: input file name
- "ShiftedSkeleton.txt" - contains input skeleton, that was transformed using counted parameters (rotation, translation, scaling)
