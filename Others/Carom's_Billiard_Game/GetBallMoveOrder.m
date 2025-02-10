function [FirstBall,SecondBall,LastBall, NbBallsMoved] = GetBallMoveOrder(Xr,Yr,Xy,Yy,Xw,Yw,MoveDistPx)

[Red_Idx,Red_Seg] = GetFirstMoveIdx(Xr,Yr,MoveDistPx);
[Yellow_Idx,Yellow_Seg] = GetFirstMoveIdx(Xy,Yy,MoveDistPx);
[White_Idx,White_Seg] = GetFirstMoveIdx(Xw,Yw,MoveDistPx);

NbBallsMoved = length([Red_Idx,Yellow_Idx,White_Idx]);

if isempty(Red_Idx) == 1
    Red_Idx = length(Xw) + 1;
end
if isempty(Yellow_Idx) == 1
    Yellow_Idx = length(Xw) + 1;
end
if isempty(White_Idx) == 1
    White_Idx = length(Xw) + 1;
end


Idx_Matrix = [1,Red_Idx, Red_Seg(find(Red_Seg,1))
              2,Yellow_Idx, Yellow_Seg(find(Yellow_Seg,1))
              3,White_Idx, White_Seg(find(Yellow_Seg,1))];
%Treat the empty case and check the first segment vector

% Sorting with respect to the second column of Idx_Matrix. If two indices
% are equal, tie is broken by the third column (initial distance)

A = sortrows(Idx_Matrix,[2 -3]);

FirstBall = A(1,1);
SecondBall = A(2,1);
LastBall = A(3,1);

end