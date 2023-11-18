% Uses standard subtract to establish dimension between two points (manhattan metric)
function [J, transformedCloud, winningTemplateIndex] = fitnessFun1(X, unknownCloud, templateClouds, removeLastRow)
[transformedCloud] = fitnessFunBase(X, unknownCloud, true);

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

    Js(templateIndex, 1) = sum(abs(tempC - transC), 'all');
end
[J, winningTemplateIndex] = min(Js);