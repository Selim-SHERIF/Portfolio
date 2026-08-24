Folder = 'T4';
Xr = [686 686 686 686 686 686 685 686 685 685 686 686 686 686 686 686 686 686 686 686 686 686 686 686 685 685 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 685 686 685 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 685 685 685 685 685 685 686 685 685 685 685 685 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686 686
];
Yr = [243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243 243
];
Xy = [180 180 180 180 179 171 157 153 144 140 127 127 129 133 142 146 153 154 161 166 168 171 179 182 185 189 196 199 202 206 212 216 219 222 231 232 235 238 245 248 251 253 257 257 259 260 263 264 257 248 232 224 218 212 200 193 187 181 169 163 157 153 140 133 127 128 137 140 143 146 153 155 158 161 167 170 173 176 182 185 187 192 196 199 202 205 210 213 218 219 224 227 231 232 236 238 240 244 247 249 251 253 258 259 261 263 270 270 271 273 278 280 283 284 288 290 292 296 297 299 301 302 309 308 310 312 315 317 319
];
Yy = [181 181 181 181 186 208 249 270 289 307 343 360 375 377 354 343 333 324 307 298 290 282 265 257 249 240 225 217 208 200 184 176 168 160 144 136 128 120 105 97 89 91 102 107 111 115 124 128 134 141 152 158 164 170 181 187 193 198 209 215 221 226 237 243 249 253 260 264 268 272 280 284 288 292 299 303 307 311 319 322 326 330 337 341 345 348 356 359 363 367 374 377 380 378 373 371 369 367 363 361 360 358 354 352 350 348 344 342 341 338 335 333 331 329 325 324 322 321 317 315 313 312 309 307 305 303 300 298 297
];
Xw = [131 131 148 170 194 223 281 309 338 365 422 449 476 504 558 585 609 631 675 697 719 718 680 662 644 627 595 580 565 551 524 512 500 487 463 451 439 426 402 390 378 367 345 335 324 313 291 281 279 279 277 275 273 271 266 263 261 259 254 252 250 247 243 241 239 236 232 230 228 225 221 219 217 215 211 208 206 204 200 198 196 194 190 188 186 184 180 178 176 174 171 169 167 165 161 160 158 156 152 151 149 147 144 142 140 139 135 133 132 130 127 128 129 130 131 132 133 133 135 136 136 137 138 139 140 140 141 142 143
];
Yw = [88 88 112 145 170 181 206 219 233 247 277 293 309 326 359 376 372 358 332 320 308 297 276 266 256 246 227 219 210 201 185 177 169 162 146 138 131 123 108 100 93 88 98 103 107 111 120 124 126 127 131 133 135 138 142 144 146 148 153 155 157 159 163 165 167 169 173 175 177 179 183 185 187 189 193 194 196 198 202 204 206 208 211 213 214 216 220 221 223 225 228 230 232 233 237 239 240 242 245 246 248 250 253 254 256 257 260 262 263 264 267 269 271 273 277 279 281 283 286 288 290 292 296 297 299 301 304 306 307
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