%% Settings
% (Note! Don't call "clear", since it will erase passed input arguments - specified in workspace)
close all;
clc;

%% Preprocess steps
% Create input and output dirs (if doens't exists)
if ~exist("input", "dir")
    mkdir("input");
end

if ~exist("output", "dir")
    mkdir("output");
end

%% Variables
% Specifying "inputFileName" value, if not passed as input argument
defaultInputFileName = "P2_A_M.txt";
if ~exist('inputFileName','var')    
    inputFileName = defaultInputFileName;
    disp("Setting default 'inputFileName' to: " + inputFileName);
else
    disp("Using passed 'inputFileName': " + inputFileName);
end

% Specifying "isMediaPipe" value, if not passed as input argument
% Note! Change 'useMediaPipe' setting to 'true' or 'false'. It determines whether to use MediaPipe or OpenPose template data
defaultUseMediaPipe = true;
if ~exist('useMediaPipe','var')
    useMediaPipe = defaultUseMediaPipe;
    disp("Setting default 'useMediaPipe' to: " + useMediaPipe);
else
    % Convert string to boolean
    if ~islogical(useMediaPipe)
        useMediaPipe = str2num(useMediaPipe);
    end
    disp("Using passed 'isMediaPipe': " + useMediaPipe);
end

% Output skeleton file name
outputSkeletonFileName = "TransformedSkeleton.txt";

% Output classified letter file name
outputClassifiedLetterFileName = "ClassifiedLetter.txt";

%% Load templates
tempFolderName = "templates/OpenPose/";
if useMediaPipe == true
    tempFolderName = "templates/MediaPipe/";
end

tempCloudNames = [
    tempFolderName+"P11_A.txt";
    tempFolderName+"P11_B.txt";
    tempFolderName+"P11_C.txt";
    tempFolderName+"P11_D.txt";
    tempFolderName+"P11_E.txt";
    tempFolderName+"P11_F.txt";
    tempFolderName+"P11_H.txt";
    tempFolderName+"P11_I.txt";
    tempFolderName+"P11_L.txt";
    tempFolderName+"P11_M.txt";
    tempFolderName+"P11_N.txt";
    tempFolderName+"P11_O.txt";
    tempFolderName+"P11_P.txt";
    tempFolderName+"P11_R.txt";
    tempFolderName+"P11_W.txt";
    tempFolderName+"P11_Y.txt";
];

templateClouds = cell(size(tempCloudNames));
templatesCloudsLength = numel(templateClouds);
for i=1:templatesCloudsLength
    templateClouds{i}=loadSkeleton(tempCloudNames(i));
end

templateNames = { ...
    'A'; ...
    'B'; ...
    'C'; ...
    'D'; ...
    'E'; ...
    'F'; ...
    'H'; ...
    'I'; ...
    'L'; ...
    'M'; ...
    'N'; ...
    'O'; ...
    'P'; ...
    'R'; ...
    'W'; ...
    'Y'; ...
};

%% Load input skeleton
inputFilePath = "input/" + inputFileName;
if ~exist(inputFilePath, "file")
    ME = MException("MATLAB:NoFile", "ERROR: Given input file doesn't exist in 'input' folder");
    throw(ME);
end

inputCloud = loadSkeleton("input/" + inputFileName);

%% Specify evolutional algorithm parameters (simulated annealing)
lb = [-320; -240; -180; 0.75; 0.75];
ub = [320; 240; 180; 1.25; 1.25];
x0 = [0, 0, 0, 1, 1];

% for OepnPose data
maxFunctionEvaluations = 50;
maxIterations = 20;
annealingFcn = "annealingfast";
temperatureFcn = "temperatureboltz";
initTemp = 50;
fitnessFunc = @(X, uc, tc) fitnessFun2(X, uc, tc, ~useMediaPipe); % Set last parameter to true, when is used OpenPose data

% for MediaPipe data
if useMediaPipe == true
    maxFunctionEvaluations = 400;
    maxIterations = 500;
    annealingFcn = "annealingboltz";
    temperatureFcn = "temperatureboltz";
    initTemp = 150;
    fitnessFunc = @(X, uc, tc) fitnessFun2(X, uc, tc, ~useMediaPipe); % Set last parameter to true, when is used OpenPose data
end

%% START OF EVOLUTIONAL SCRIPT
% Prepare 'optimizationOptions' structure (there aren't available 'UseParallel' and 'UseVectorized' options for 'simulannealbnd' optimoptions)
optimizationOptions = optimoptions( ...
    'simulannealbnd', ...
    'Display', 'off', ...
    'MaxFunctionEvaluations', maxFunctionEvaluations, ...
    'MaxIterations', maxIterations, ...
    'AnnealingFcn', annealingFcn, ...
    'TemperatureFcn', temperatureFcn, ...
    'InitialTemperature', initTemp ...
);

% Start the timer
tStart = tic;

rng default; % can be commented
fitnessFunLambda = @(X) fitnessFunc(X, inputCloud, templateClouds);
[Xmin, Jmin] = simulannealbnd(fitnessFunLambda, x0, lb, ub, optimizationOptions);
[~, transformedCloud, winingTemplateIndex] = fitnessFunLambda(Xmin);
recognizedClass = templateNames{winingTemplateIndex, 1};

% Stop the timer and print time results
tEnd = toc(tStart);
tEndMin = floor(tEnd / 60);
tEndSec = floor(mod(tEnd, 60));
elapsedTimeStr = "Elapsed time of predicting: "+tEndMin+" min "+tEndSec+" sec; In seconds: "+tEnd+" sec";
disp(elapsedTimeStr);

%% Saving results to files
% Save transformed input skeleton
transformedInputCloudToSave = transformedCloud.Location(:, 1:2);

if useMediaPipe == false % Remove last row when using OpenPose data
    newLength = length(transformedInputCloudToSave) - 1;
    transformedInputCloudToSave = transformedInputCloudToSave(1:newLength, 1:2);
end

transformedInputCloudToSave = round(transformedInputCloudToSave * 100) / 100; % Round number to 2 decimal places
writematrix(transformedInputCloudToSave, "output/" + outputSkeletonFileName, 'Delimiter', ' ');

% Save recognized class
writelines([recognizedClass; "Input file name: " + inputFileName], "output/" + outputClassifiedLetterFileName, WriteMode="overwrite");

disp("Results were saved to output folder");
disp("**---- END OF SCRIPT ----**");