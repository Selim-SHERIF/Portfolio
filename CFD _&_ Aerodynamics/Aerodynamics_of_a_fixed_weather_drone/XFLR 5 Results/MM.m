syms AB BB X1 X2 
vpasolve( 0.75== 0.5 + AB*cosd(X1)+ BB , AB*sind(X1) == 1.5, 0.75 == 0.4829629131 + AB *cosd(X2), 1.5 == 0.1294095 + AB*sind(X2)-BB)