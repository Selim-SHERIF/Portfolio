function [X,Y] = RemoveOutlier(X,Y)

Out_X = isoutlier(X,'movmedian',10);
Out_Y = isoutlier(Y,'movmedian',10);

Out_Idx = find(Out_X + Out_Y == 2);

Out_Idx(Out_Idx == 1) = [];

if(isempty(Out_Idx) == 0)
X(Out_Idx) = X(Out_Idx - 1);
Y(Out_Idx) = Y(Out_Idx - 1);

end 
