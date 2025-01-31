Folder = 'T1';
Xr = [667 667 667 651 621 559 531 NaN 471 419 400 379 361 323 304 287 270 235 219 203 187 154 137 129 143 168 181 192 203 224 233 244 252 271 279 287 297 314 323 331 341 357 367 375 383 401 410 419 426 443 452 461 469 487 495 504 511 529 537 545 555 571 579 587 595 611 619 628 635 648 655 661 667 679 685 691 699 712 718 723 725 715 712 709 705 699 696 692 689 683 679 677 674 668 665 661 659 653 650 646 644 639 635 633 629 624 621 618 616 610 607 604 601 596 594 591 588 583 580 577 576 570 568 565 563 558 555 552 550 545 543 540 538 533 532 529 527 522 519 517 515 511 508
];
Yr = [211 211 211 221 245 289 313 NaN 351 375 357 341 325 293 281 269 253 229 217 205 193 173 161 149 139 117 105 94 87 105 113 120 127 139 145 151 157 169 175 181 185 198 205 210 215 227 233 239 245 257 261 267 273 285 291 295 301 313 319 325 329 341 345 351 357 369 373 379 379 369 367 365 361 357 355 353 349 344 341 339 337 335 335 333 333 331 331 329 329 327 326 325 325 323 321 321 320 318 317 317 317 315 313 313 312 311 310 309 308 307 306 305 305 303 303 301 301 299 299 299 297 295 295 295 295 293 291 291 291 289 289 287 287 285 285 284 283 283 281 281 281 279 279
];
Xy = [718 NaN NaN 682 692 712 721 725 716 704 702 691 682 664 656 647 637 621 612 604 596 579 571 562 556 537 530 520 513 496 488 480 471 455 447 440 435 426 419 414 409 400 392 387 381 370 365 361 355 344 339 335 328 318 313 309 302 292 287 283 277 267 262 257 252 244 236 231 227 218 212 207 205 192 187 182 179 168 166 158 154 145 140 135 131 128 131 134 137 141 143 146 148 153 158 159 157 159 160 161 162 163 166 166 166 168 168 169 170 170 171 172 172 174 174 175 176 179 179 179 179 180 181 181 182 183 184 184 185 186 186 187 187 188 188 192 192 192 192 192 192 193 193
];
Yy = [125 NaN NaN 213 232 267 284 302 321 356 372 379 364 337 325 313 300 279 270 260 251 233 224 215 206 188 179 170 161 143 134 125 117 98 90 91 99 111 116 121 125 133 137 142 146 154 158 162 166 174 178 182 187 194 198 203 206 214 218 223 226 234 238 242 246 253 257 261 265 273 277 281 285 292 296 299 303 310 314 318 321 329 333 336 340 346 348 351 353 358 360 363 365 370 372 375 377 379 378 377 375 372 371 370 369 365 364 363 362 359 358 357 356 354 353 351 350 348 346 346 345 343 342 340 339 338 337 335 335 333 332 331 330 328 327 327 326 325 324 323 322 321 320
];
Xw = [169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 169 170 169 171 172 173 175 176 176 178 179 180 181 183 184 185 185 187 188 188 189 191 192 192 193 194 195 196 196 197 198 198 199 200 201 201 201 202 203 203 203 205 205 205 205 206 206 206 206 207 207
];
Yw = [367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 367 368 368 368 368 368 368 368 368 368 368 368 368 368 368 368 368 367 367 366 366 366 366 366 366 365 365 365 365 365 365 365 365 365 365 365 365 365 365 364 364 364 364 364 364 364 363 363 363 363 363 363 363 363 363 362 362 362 362 362 362 362 362 362
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