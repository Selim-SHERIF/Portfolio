Folder = 'T9';
Xr = [267 267 266 255 251 241 235 227 223 215 211 203 199 192 188 184 183 181 180 177 175 173 174 169 168 166 165 163 161 159 157 155 153 151 149 147 145 143 143 140 140 137 137 135 135 134 134 132 131 131 130 129 128 127 127 129 129 129 130 129 130 131 131 131 131 133 133 134 134 135 135 136 136 136 136 137 137 138 138 139 139 139 140 141 140 141 141 142 143 143 143 143 144 144 144 145 145 146 146 146 147 147 147 147 147 147 147 147 147 148 149 149 149 149 149 149 150 150 150 151 151 151 151 151 151 151 151 151 151 152 152 152 152 152 152 152 153 153 152 153 153 153 153 153 154 153
];
Yr = [377 377 377 349 329 293 274 241 225 197 181 153 139 109 95 101 111 131 141 157 165 181 189 203 209 225 231 245 253 269 275 289 297 311 317 331 339 353 359 373 379 368 364 355 352 345 339 331 329 321 317 309 305 298 294 287 285 277 273 267 263 257 253 246 243 237 233 227 223 217 213 207 204 198 195 189 186 180 177 171 167 162 159 153 151 145 142 137 133 128 125 121 117 112 109 105 101 97 93 89 89 89 90 93 95 97 98 101 102 105 107 109 110 113 113 117 117 119 121 123 125 127 127 129 131 133 133 135 136 137 139 140 141 143 143 145 145 147 147 149 150 151 152 153 153 155
];
Xy = [712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 127 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 712 713 716 718 721 722 725 726 725 724 722 721 720 719 718 717 716 715 714 714 713 712 712 712 712 709 708 708 707 706 705
];
Yy = [167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 194 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 167 166 166 166 166 166 166 166 166 166 166 166 166 166 166 166 166 166 166 166 166 166 166 166 166 166 166 167 168 170 171 172 173 174 175 176 177 177 178 179 179 180 181 181 182 182 183 183 184 185 185 186 186 186 187 187 188
];
Xw = [251 251 267 316 342 394 419 469 493 539 563 609 632 678 701 721 694 657 639 606 590 560 546 520 508 485 473 451 439 417 405 383 371 348 337 314 302 279 268 245 234 211 200 177 166 144 132 139 148 164 171 183 189 201 207 219 225 237 243 254 260 272 278 289 295 307 312 324 330 341 347 358 364 375 380 392 397 408 413 424 430 441 446 457 462 473 478 489 494 505 510 520 526 536 541 551 556 566 572 581 587 597 602 612 616 626 631 641 646 655 660 670 675 684 689 698 702 707 710 716 718 724 726 725 723 720 719 716 715 711 709 705 703 699 697 694 692 688 686 683 681 677 675 672 670 667
];
Yw = [328 329 359 380 373 361 355 345 340 333 329 323 320 313 310 303 289 269 260 242 232 214 206 189 180 163 155 138 130 113 105 89 90 102 107 116 121 129 133 142 147 156 160 169 172 181 185 197 204 216 222 234 240 253 258 270 276 288 294 306 312 324 330 341 347 359 364 376 379 370 367 360 357 351 347 341 337 331 328 322 318 312 309 303 299 293 290 284 281 274 272 265 262 256 253 247 244 238 235 229 226 221 218 212 209 203 200 194 192 186 183 177 175 169 166 161 157 150 146 138 135 127 124 116 113 105 102 95 91 89 92 95 97 101 103 107 109 113 115 118 120 124 126 129 131 135
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