function PathLength = GetBallPathLength(X,Y)

dX = diff(X);
dY = diff(Y);

PathLength = sum(sqrt(dX.^2 + dY.^2));

end