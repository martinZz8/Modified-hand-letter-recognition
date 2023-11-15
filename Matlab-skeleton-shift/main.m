%% settings
close all;
clear;
clc;

%% load data
inFName = "input";
outFName = "output";
inputDataFolderNames = [inFName + "/OpenPose"; inFName + "/MediaPipe"];
letterNames = [...
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
];
personNums = 1:11;

% Perform shift on every cloud and save it to new location
for currInputFolderNameIdx=1:length(inputDataFolderNames)
    disp("-- Started folder "+ inputDataFolderNames(currInputFolderNameIdx) + " --");
    currOutputFolderName = replace(inputDataFolderNames(currInputFolderNameIdx), inFName, outFName);

    for currLetterNameIdx=1:length(letterNames)
        disp("- Started letter "+ letterNames(currLetterNameIdx) + " -");
        for currPersonNumIdx=1:length(personNums)
            % Get current path of skeleton
            currLoadPath = inputDataFolderNames(currInputFolderNameIdx) + "/" + letterNames(currLetterNameIdx) + "/" + combineFileName(personNums(currPersonNumIdx), letterNames(currLetterNameIdx));
            
            % Load skeleton (if file exists)
            if exist(currLoadPath, "file")
                pcSkeleton = loadSkeleton(currLoadPath);

                % If skeleton isn't empty, shift it
                if ~isempty(pcSkeleton)
                    pcShiftedSkeleton = shiftCloud(pcSkeleton);
    
                    % Create folder if doesn't exist
                    saveFolderPath = currOutputFolderName + "/" + letterNames(currLetterNameIdx);
                    if ~exist(saveFolderPath, "dir")
                        mkdir(saveFolderPath);
                    end
    
                    % Save skeleton to specified location
                    currSavePath = currOutputFolderName + "/" + letterNames(currLetterNameIdx) + "/" + combineFileName(personNums(currPersonNumIdx), letterNames(currLetterNameIdx));
                    writematrix(pcShiftedSkeleton.Location, currSavePath, "Delimiter", ' ');
                end
            end            
        end
    end
end
disp("END")