function [cloud] = loadSkeleton(skeletonFile)
skeletonData = importdata(skeletonFile);
[nodesCount, ~] = size(skeletonData);
cloud = pointCloud([skeletonData zeros(nodesCount, 1)]);