function [IdxTouch] = GetTouchIdx(X,Y,Xmin,Xmax,Ymin,Ymax,BallBorderDist)

IdxTouch = [];

% Eliminating first index if it satisfies the rebound condition

if X(1) + BallBorderDist >= Xmax || X(1) - BallBorderDist <= Xmin
    X(1) = []; 
else 
    if Y(1) + BallBorderDist >= Ymax || Y(1) - BallBorderDist <= Ymin
        Y(1) = [];
    end
end

% rebound is a logical vector of zeros and ones
% the find function allows to search for the index of the first ones that appear
% in the logical vector

rebound = X + BallBorderDist >= Xmax; % right
IdxTouch = [IdxTouch, 1 + find(diff(rebound) == 1)];

rebound = Y + BallBorderDist >= Ymax; % top
IdxTouch = [IdxTouch, 1 + find(diff(rebound) == 1)];

rebound = X - BallBorderDist <= Xmin; % left
IdxTouch = [IdxTouch, 1 + find(diff(rebound) == 1)];

rebound = Y - BallBorderDist <= Ymin; % bottom
IdxTouch = [IdxTouch, 1 + find(diff(rebound) == 1)];

IdxTouch = unique(IdxTouch);

end


            
