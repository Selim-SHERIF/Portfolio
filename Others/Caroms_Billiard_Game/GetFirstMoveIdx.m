function [FirstMoveIdx,MoveDist] = GetFirstMoveIdx(X,Y,MoveDistPx)

% Computing the horizontal and vertical distances to X(1)

X = X - X(1);
Y = Y - Y(1);

d = sqrt(X.^2 + Y.^2); 

% Searching for the first index that verifies the condition d > MoveDistPx

FirstMoveIdx = find(d > MoveDistPx, 1);

MoveDist = sqrt(diff(X).^2 + diff(Y).^2);

end