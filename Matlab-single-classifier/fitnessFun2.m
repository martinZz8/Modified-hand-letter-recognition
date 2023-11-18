% Uses euclidean function to establish dimension between two points (euclidean metric)
function [J, transformedCloud, winningTemplateIndex] = fitnessFun2(X, unknownCloud, templateClouds, removeLastRow)
[transformedCloud] = fitnessFunBase(X, unknownCloud, true);

% exclude last point in last index (duplicated point on smallest finger)
templatesCount = numel(templateClouds);
Js = zeros(templatesCount, 1);
for templateIndex=1:templatesCount
    tempC = templateClouds{templateIndex}.Location(:,1:2);
    transC = transformedCloud.Location(:,1:2);

    if removeLastRow == true
        [numPoints,~] = size(tempC);
        newNumPoints = numPoints - 1; % exclude last point in last index (duplicated point on smallest finger)
        tempC = tempC(1:newNumPoints,1:2);
        transC = transC(1:newNumPoints,1:2);
    end

    diffsCloud = abs(tempC - transC);
    for i=1:length(diffsCloud)
        euclideanLength = sqrt(diffsCloud(i,1)^2 + diffsCloud(i,2)^2);
        Js(templateIndex, 1) = Js(templateIndex, 1) + euclideanLength;
    end
end
[J, winningTemplateIndex] = min(Js);