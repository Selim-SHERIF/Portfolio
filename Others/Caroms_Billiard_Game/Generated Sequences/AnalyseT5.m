Folder = 'T5';
Xr = [230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 230 225 221 213 210 206 203 195 192 189 185 179 175 172 168 162 158 155 151 145 142 139 136 129 128 131 131 136 137 139 140 144 145 147 149 151 153 155 156 159 161 163 164 167 168 170 172 175 176 178 179 182 183 184 186 189 190 191 193 195 196 198 199 201 202 203 205 207 209 209 211 213 213
];
Yr = [161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 161 165 168 174 177 179 183 189 190 193 195 200 203 206 209 213 216 219 221 225 228 231 233 238 241 241 243 247 249 251 251 255 257 258 259 263 264 266 267 270 271 273 274 277 278 280 282 285 286 287 289 291 293 293 295 297 299 300 301 304 305 306 307 309 311 312 313 315 317 317 319 321 321
];
Xy = [243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 243 243 243 243 243 243 243 243 243 243 243 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244 244
];
Yy = [136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136 136
];
Xw = [239 239 239 239 245 265 284 302 340 359 378 397 434 453 472 491 527 545 563 580 616 635 652 670 705 723 720 705 676 663 651 641 621 612 603 595 578 569 560 552 535 526 518 509 492 484 476 467 451 442 434 426 409 401 393 385 368 360 352 344 328 320 312 304 288 280 272 264 248 241 237 234 227 223 219 215 208 204 200 197 189 186 182 178 171 167 164 160 153 149 146 143 136 132 129 128 133 135 137 138 142 144 146 147 151 152 154 156 159 161 162 164 167 168 169 171 173 175 176 178 180 181 182 184 186 187 188 190 192 193 194 195 197 198 199 200 202 203 204 205 207 208
];
Yw = [112 112 112 112 111 110 108 107 103 100 98 97 93 91 89 88 89 90 91 93 94 95 96 97 99 100 98 95 90 88 89 91 94 96 97 98 101 102 104 105 107 109 110 111 113 115 116 118 120 121 123 124 126 128 129 130 133 134 135 137 139 141 142 143 145 147 148 149 152 153 151 148 144 143 141 139 136 134 132 130 127 125 124 122 119 117 115 114 111 109 107 106 102 101 99 98 97 97 96 95 94 93 92 92 90 90 89 89 88 87 87 86 87 87 87 88 89 89 89 90 90 90 91 91 92 92 92 93 93 94 94 94 94 95 95 95 96 96 96 97 97 97
];
BorderWinColor = [0 255 22
];
BorderLossColor = [255 53 0
];
LineStyle = '-';
BorderHitStyle = 'o';

BallDiameter = 13;
MoveDistPx = 9;
BallBorderDist = 9;

% Assigning each ball its ID
Red_ID = 1; 
Yellow_ID = 2;
White_ID = 3;

% Finding the table borders using the get frame function 

[Xmin, Xmax, Ymin, Ymax] = GetFrame(Xr,Yr,Xy,Yy,Xw,Yw);

% Finding and replacing all NaN values with InterpolateNan function

[Xr, Yr] = InterpolateNan(Xr,Yr);
[Xy, Yy] = InterpolateNan(Xy,Yy);
[Xw, Yw] = InterpolateNan(Xw,Yw);

% Removing all outliers 

[Xr, Yr] = RemoveOutlier(Xr,Yr);
[Xy, Yy] = RemoveOutlier(Xy,Yy);
[Xw, Yw] = RemoveOutlier(Xw,Yw);

% Getting the total distance traveled by each ball 

PathLength_Red = GetBallPathLength(Xr,Yr);
PathLength_Yellow = GetBallPathLength(Xy,Yy);
PathLength_White = GetBallPathLength(Xw,Yw);

% Getting the ball move order 

[FirstBall, SecondBall, LastBall, NbBallsMoved] = GetBallMoveOrder(Xr,Yr,Xy,Yy,Xw,Yw,MoveDistPx);

% Assigning which ball was hit first

if (FirstBall == Red_ID)

    IdxTouch = GetTouchIdx(Xr,Yr,Xmin,Xmax,Ymin,Ymax,BallBorderDist);
    X1 = Xr;
    Y1 = Yr;
    Color = 'Red';

elseif (FirstBall == Yellow_ID)

        IdxTouch = GetTouchIdx(Xy,Yy,Xmin,Xmax,Ymin,Ymax,BallBorderDist);
        X1 = Xy;
        Y1 = Yy;
        Color = 'Yellow';

elseif (FirstBall == White_ID)

    IdxTouch = GetTouchIdx(Xw,Yw,Xmin,Xmax,Ymin,Ymax,BallBorderDist);
    X1 = Xw;
    Y1 = Yw;
    Color = 'White';

end

% Assigning which ball was hit second

if (SecondBall == Red_ID)
    X2 = Xr;
    Y2 = Yr;
    SecondTouch = GetFirstMoveIdx(Xr,Yr,MoveDistPx);
elseif (SecondBall == Yellow_ID)
    X2 = Yy;
    Y2 = Yy;
    SecondTouch = GetFirstMoveIdx(Xy,Yy,MoveDistPx);
elseif (SecondBall == White_ID)
    X2 = Xw;
    Y2 = Yw;
    SecondTouch = GetFirstMoveIdx(Xw,Yw,MoveDistPx);
end

% Assigning which ball was hit last

if (LastBall == Red_ID)
    X3 = Xr;
    Y3 = Yr;
elseif (LastBall == Yellow_ID)
    X3 = Xy;
    Y3 = Yy;
elseif (LastBall == White_ID)
    X3 = Xw;
    Y3 = Yw;
end

IdxTouch = IdxTouch(IdxTouch >= SecondTouch); % Taking border touches only after the second ball is hit
BorderHits = length(IdxTouch); % Counting border hits
NbBallsMoved = NbBallsMoved; % Number of balls moved

% Win or loss ? 

if NbBallsMoved == 3 && BorderHits >= 3
    Result = 'Win';
    BorderHitColor = BorderWinColor/255;
else
    Result = 'Loss';
    BorderHitColor = BorderLossColor/255;
end

% Creating score sheet

figure('Name','ScoreSheet','NumberTitle','off')
hold all

set(gcf,'color','white')
axis([Xmin Xmax 0 Ymax])
axis off

% Creating rectangle representing the frame

rectangle('Position',[Xmin Ymin Xmax-Xmin Ymax-Ymin],'EdgeColor','b','LineWidth',1)

% Plotting ball trajectories

plot(Xr,Yr,[LineStyle, 'r'],'LineWidth',1,'Marker','o','MarkerSize',1.5,'MarkerFaceColor','r')
plot(Xy,Yy,[LineStyle, 'y'],'LineWidth',1,'Marker','o','MarkerSize',1.5,'MarkerFaceColor','y')
plot(Xw,Yw,[LineStyle, 'b'],'LineWidth',1,'Marker','o','MarkerSize',1.5,'MarkerFaceColor','b')

% Plotting the first position of each ball

plot(Xr(1),Yr(1),'Marker','hexagram','MarkerSize',15,'MarkerEdgeColor','r')
plot(Xy(1),Yy(1),'Marker','hexagram','MarkerSize',15,'MarkerEdgeColor','y')
plot(Xw(1),Yw(1),'Marker','hexagram','MarkerSize',15,'MarkerEdgeColor','b')

% Plotting the border hits using the chosen BorderHitStyle and
% BorderHitColor from LabVIEW

scatter(X1(IdxTouch),Y1(IdxTouch),100,'Marker',BorderHitStyle,'MarkerEdgeColor',BorderHitColor)

% Displaying the captions of the score-sheet

t = char(datetime('now'));
title(['Score Sheet - ' Folder ' - (' t ')'],'FontSize',15);

text(Xmin + (Xmax - Xmin)*0.125,Ymin*0.75,{['Score sheet for ' '"' Color ' Ball' '"'],['--- ' Result ' ---']});

text(Xmin + (Xmax - Xmin)*0.125,Ymin*0.25,['dist(R):' num2str(int32(PathLength_Red)) 'px']);
text(Xmin + (Xmax - Xmin)*0.375,Ymin*0.25,['dist(Y):' num2str(int32(PathLength_Yellow)) 'px']);
text(Xmin + (Xmax - Xmin)*0.625,Ymin*0.25,['dist(W):' num2str(int32(PathLength_White)) 'px']);

text(Xmin + (Xmax - Xmin)*0.625,Ymin*0.75,{[num2str(NbBallsMoved) ' ball(s) touched'],[num2str(BorderHits) ' band(s) touched']}) 

hold off 

% Saving the score-sheet as a .pdf file under the format ScoreSheetTx.pdf

filename = sprintf('ScoreSheet%s',Folder);
saveas(gcf,filename,'pdf');

%% AnalyseTx.m 
% 
% Authors:
%   Roy Turk 34 55 77
%   Selim Sherif 34 60 35
%
% Script containing a combination of functions that will receive the ball 
% coordinates from LabVIEW and display the score-sheet with the final 
% result of the game.