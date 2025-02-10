function [X,Y] = InterpolateNan(X,Y)

X = [0,X];
Y = [0,Y];

NaN_X = isnan(X);
X_Idx = 1:numel(X);

X(NaN_X) =  interp1(X_Idx(~NaN_X),X(~NaN_X),X_Idx(NaN_X),'next');

NaN_Y = isnan(Y);
Y_Idx = 1:numel(Y);

Y(NaN_Y) = interp1(Y_Idx(~NaN_Y),Y(~NaN_Y),Y_Idx(NaN_Y),'next');

X = X(2:end);
Y = Y(2:end);

end

