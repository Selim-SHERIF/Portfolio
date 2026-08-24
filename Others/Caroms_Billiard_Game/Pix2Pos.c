/**

Pix2Pos.c

Combination of functions that will read the Pixmap.bin file and write an output file, Pos.txt, containing the 
coordinates of each ball and following the format:

Red: X_Red, Y_Red, Score_Red
Yellow: X_Yellow, Y_Yellow, Score_Yellow
White: X_White, Y_White, Score_White

Authors: 
    Selim Sherif, 34 60 35
    Roy Turk, 34 55 73

Platform: Windows 11
Compiler: Visual Studio Code (GCC)

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define BallminScore 15

// Structure Range defines the range for each of the red, green and blue colors
struct Range{
    int Rmin, Rmax, Gmin, Gmax, Bmin, Bmax;
};

// Structure Output contains three elements that define the position and score of each ball
struct Output{
    int X, Y, Score;
};

// Structure PNG contains the properties of the image that will be analyzed
struct PNG{
    unsigned int Width, Height;
};

// Structure Pixel contains the properties of each pixel defining red, green and blue
struct Pixel{
    unsigned int R,G,B;
};

// Functions used in the main, cf. end of file for function definition
void HEXtoRGB(unsigned int PIX, struct Pixel *RGB);
int RangeTest(unsigned int PIX, struct Range Color);
void SquareScore(int Square_Y, int Square_X, int Width, unsigned int *Pixel, struct Range Red, struct Range Yellow, struct Range White, int *RedScore_ptr, int *YellowScore_ptr, int *WhiteScore_ptr, int BallDiameter);
void BallLocator(int Lmin, int Lmax, int Cmin, int Cmax, int BallDiameter, int Width, unsigned int *Pix, struct Output *RedBall, struct Output *YellowBall, struct Output *WhiteBall, struct Range Red, struct Range Yellow, struct Range White, struct Range Blue);

int main(int argc, const char* argv[]){

    if((argc-1) != 29){ // Checking if the correct number of arguments in entered

        fprintf(stderr, "Error! Incorrect number of arguments!\n"); 
        return 1;
    }

    struct Range Red, Yellow, White, Blue; // Color ranges

    struct Output RedBall = {-1,-1,0}, YellowBall = {-1,-1,0}, WhiteBall = {-1,-1,0}; // Initializing position and score for each ball
    struct Output *RedPointer = &RedBall, *YellowPointer = &YellowBall, *WhitePointer = &WhiteBall; // Assigning pointers to each ball
    
    struct PNG Image = {0,0}; // Initializing image width and height

    int Lmin, Lmax, Cmin, Cmax, BallDiameter; // Table limits and ball diameter

    Lmin = atoi(argv[1]); // Assigning table limits
    Lmax = atoi(argv[2]);
    Cmin = atoi(argv[3]);
    Cmax = atoi(argv[4]);

    Red.Rmin = atoi(argv[5]); // Assigning red color ranges
    Red.Rmax = atoi(argv[6]);
    Red.Gmin = atoi(argv[7]);
    Red.Gmax = atoi(argv[8]);
    Red.Bmin = atoi(argv[9]);
    Red.Bmax = atoi(argv[10]);

    Yellow.Rmin = atoi(argv[11]); // Assigning yellow color ranges
    Yellow.Rmax = atoi(argv[12]);
    Yellow.Gmin = atoi(argv[13]);
    Yellow.Gmax = atoi(argv[14]);
    Yellow.Bmin = atoi(argv[15]);
    Yellow.Bmax = atoi(argv[16]);

    White.Rmin = atoi(argv[17]); // Assigning white color ranges
    White.Rmax = atoi(argv[18]);
    White.Gmin = atoi(argv[19]);
    White.Gmax = atoi(argv[20]);
    White.Bmin = atoi(argv[21]);
    White.Bmax = atoi(argv[22]);

    Blue.Rmin = atoi(argv[23]); // Assigning blue color ranges
    Blue.Rmax = atoi(argv[24]);
    Blue.Gmin = atoi(argv[25]);
    Blue.Gmax = atoi(argv[26]);
    Blue.Bmin = atoi(argv[27]);
    Blue.Bmax = atoi(argv[28]);

    BallDiameter = atoi(argv[29]); // Assigning ball diameter

    if(BallDiameter < 5 || BallDiameter > 20){ // Checking if we have a correct ball diameter

        fprintf(stderr, "Error! Incorrect ball diameter!\n");
        return 1;
    }

    FILE *PIXMAP;
    
    PIXMAP = fopen("Pixmap.bin", "rb"); // Opening Pixmap.bin file and reading in binary mode

    if(PIXMAP == NULL){ // Checking for error while opening file

        fprintf(stderr, "Error! Cannot open Pixmap.bin!\n");
        return 2;
    }

    if((fread(&Image, sizeof(Image), 1, PIXMAP) != 1)){

        if(ferror(PIXMAP)){

            fprintf(stderr, "Error! Problem reading Pixmap.bin!\n");
            return 2;
        }
        else if(feof(PIXMAP)){

            fprintf(stderr, "Error! EOF reached! Could not get image properties!\n");
            return 2;
        }
    }

    if(Image.Width < 100 || Image.Width > 1000){ // Checking if we have a correct image width

        fprintf(stderr, "Error! Not a valid image width!\n");
        return 1;
    }

    if(Image.Height < 100 || Image.Height > 1000){ // Checking if we have a correct image height

        fprintf(stderr, "Error! Not a valid image height!\n");
        return 1;
    }

    unsigned int *Pix = malloc(Image.Width*Image.Height*sizeof(unsigned int)); // Memory allocation for elements of Pixmap.bin

    if(Pix == NULL){

        fprintf(stderr, "Error! Problem allocating memory!\n");
        return 4;
    }

    if(fread(Pix, sizeof(unsigned int), Image.Width*Image.Height, PIXMAP) < Image.Width*Image.Height){ // Filling Pix with the elements of pixmap.bin and checking if there are enough pixels

        if(ferror(PIXMAP)){
            
            fprintf(stderr, "Error! Problem reading Pixmap.bin!\n");
            return 2;
        }
        else if(feof(PIXMAP)){

            fprintf(stderr, "Error! EOF reached! Not enough pixels!\n");
            return 2;
        }
    }

    int i = 0;

    if(fread(&i, sizeof(int), 1, PIXMAP)){ // Checking if there are more elements than necessary

        fprintf(stderr, "Warning! Passed pixel limit!\n");
    }

    if(fclose(PIXMAP)){ // Closing the Pixmap.bin file and checking for any errors

        fprintf(stderr, "Error! Could not close Pixmap.bin file!\n");
        return 2;
    }

    // Finding each ball coordinates and score with the BallLocator function
    BallLocator(Lmin, Lmax, Cmin, Cmax, BallDiameter, Image.Width, Pix, RedPointer, YellowPointer, WhitePointer, Red, Yellow, White, Blue);

    // Warning if any ball is missing 
    if(RedBall.Score == 0){
        fprintf(stderr,"Warning! Red ball missing!\n");
    }
    if(YellowBall.Score == 0){
        fprintf(stderr, "Warning! Yellow ball missing!\n");
    }
    if(WhiteBall.Score == 0){
        fprintf(stderr, "Warning! White ball missing!\n");
    }
    
    free(Pix);

    FILE *POS;

    POS = fopen("Pos.txt", "w"); // Opening the Pos.txt file in writing mode

    if(POS == NULL){ // Checking for error while opening the file

        fprintf(stderr, "Error! Could not open Pos.txt file!\n");
        return 3;
    }

    // Writing the pos.txt file in the format specified at the beginning of the file 
    if(fprintf(POS, "Red: %d, %d, %d\nYellow: %d, %d, %d\nWhite: %d, %d, %d\n\n", RedBall.X, RedBall.Y, RedBall.Score, YellowBall.X, YellowBall.Y, YellowBall.Score, WhiteBall.X, WhiteBall.Y, WhiteBall.Score) < 0){

        fprintf(stderr, "Error! Could not write properly in Pos.txt file!\n"); // Checking for any errors while writing the file
        return 3;
    }

    if(fclose(POS)){ // Closing the Pos.txt file and checking for any errors

        fprintf(stderr, "Error! Could not close Pos.txt file!\n");
        return 3;
    }

    return 0;
}

/**

HEXtoRGB 

Function that extracts the red, green and blue values from the Pixmap.bin file. It uses masking and bit shifting in
order to store the colors in the RGB variable. 

Arguments: 
    PIX: representation of a pixel
    RGB: variable of struct Pixel containing integers for R,G and B colors

Return:
    N/A (void function)

*/

void HEXtoRGB(unsigned int PIX, struct Pixel *RGB){

    RGB -> R = (PIX >> 16) & 0xFF;
    RGB -> G = (PIX >> 8) & 0xFF;
    RGB -> B = PIX & 0xFF;
    
}

/**

RangeTest

Function that tests if each of the pixel colors is within the given range.

Arguments:
    PIX: representation of a pixel
    Color: variable of struct Color that will be used for the range test

Return:
    1 if the test is successful and the pixel is in the color range
    0 if the test failed and the pixel is not in the color range

*/

int RangeTest(unsigned int PIX, struct Range Color){

    struct Pixel TestPixel = {0,0,0}; // Initializing the pixel that will be tested 
    struct Pixel *TestPixel_ptr = &TestPixel;

    HEXtoRGB(PIX, TestPixel_ptr); // Calling the HEXtoRGB function to extract the pixel properties

    return ((*TestPixel_ptr).R >= Color.Rmin && (*TestPixel_ptr).R <= Color.Rmax &&
            (*TestPixel_ptr).G >= Color.Gmin && (*TestPixel_ptr).G <= Color.Gmax &&
            (*TestPixel_ptr).B >= Color.Bmin && (*TestPixel_ptr).B <= Color.Bmax);
}

/**

SquareScore

This function calculates the score of the area analyzed.

Arguments: 
    Square_X, Square_Y: location of the first pixel in the square
    Width: image width
    Pixel: pointer to the pixels in the array
    Red, Yellow, White: variables of struct Range
    RedScore_ptr, YellowScore_ptr, WhiteScore_ptr: score for each color
    BallDiameter: integer representing the given ball diameter

Return:
    N/A (void function)

*/

void SquareScore(int Square_Y, int Square_X, int Width, unsigned int *Pixel, struct Range Red, struct Range Yellow, struct Range White, int *RedScore_ptr, int *YellowScore_ptr, int *WhiteScore_ptr, int BallDiameter){

    *RedScore_ptr = 0;
    *YellowScore_ptr = 0;
    *WhiteScore_ptr = 0;

    for(int i = Square_Y; i < Square_Y + BallDiameter; i++){
        for(int j = Square_X; j < Square_X + BallDiameter; j++){

            *RedScore_ptr += RangeTest(*(Pixel + i*Width + j), Red);
            *YellowScore_ptr += RangeTest(*(Pixel + i*Width + j), Yellow);
            *WhiteScore_ptr += RangeTest(*(Pixel + i*Width + j), White);
        }
    }
}

/**

Ball Locator

Function that tries to locate each ball in the given limits and assigns a score. At the end each ball is given the
three members of the struct Output: the X and Y coordinates and the score.

Arguments:
    Lmin, Lmax, Cmin, Cmax: the limits in which the function will locate the balls
    BallDiameter: integer representing the given ball diameter
    Width: image width
    RedBall, YellowBall, WhiteBall: variables of struct Output
    Red, Yellow, White, Blue: variables of strut Range

Return:
    N/A (void function)
*/

void BallLocator(int Lmin, int Lmax, int Cmin, int Cmax, int BallDiameter, int Width, unsigned int *Pix, struct Output *RedBall, struct Output *YellowBall, struct Output *WhiteBall, struct Range Red, struct Range Yellow, struct Range White, struct Range Blue){

    int RedScore = 0, YellowScore = 0, WhiteScore = 0; // Initializing each score
    int *RedScore_ptr = &RedScore, *YellowScore_ptr = &YellowScore, *WhiteScore_ptr = &WhiteScore;
    int Square_X, Square_Y;

    int *Speed = calloc(Width, sizeof(int));

    for(Square_Y = Lmin; Square_Y <= Lmax - BallDiameter + 1; Square_Y++){
        for(Square_X = Cmin; Square_X <= Cmax - BallDiameter + 1; Square_X++){

            if(*(Speed + Square_X) >= 1){

                if(*(Speed + Square_X) == BallDiameter){

                    *(Speed + Square_X) = 0;
                }
                if(*(Speed + Square_X + BallDiameter) >= 1){

                    for(int i = Square_X; i < Square_X + BallDiameter; i++){

                        if(*(Speed + i) >= 1){

                            *(Speed + i) += 1;

                            if(*(Speed + i) == BallDiameter){

                                *(Speed + i) = 0;
                            }
                        }
                    }
                    *(Speed + Square_X) += 1;
                    Square_X += BallDiameter;
                }
            }

            SquareScore(Square_Y, Square_X, Width, Pix, Red, Yellow, White, RedScore_ptr, YellowScore_ptr, WhiteScore_ptr, BallDiameter);

            if(RedScore == 0 && YellowScore == 0 && WhiteScore == 0){

                if(Square_X <= Cmax - 2 * BallDiameter + 1){

                    for(int i = Square_X; i < Square_X + BallDiameter; i++){

                        if(*(Speed + i) >= 1){

                            *(Speed + i) += 1;

                            if(*(Speed + i) == BallDiameter){

                                *(Speed + i) = 0;
                            }
                        }
                    }
                    Square_X += BallDiameter - 1;
                }
                else{

                    if(Square_X == Cmax - BallDiameter + 1){

                        *(Speed + Square_X) += 1;

                        if(*(Speed + Square_X) == BallDiameter){

                            *(Speed + Square_X) = 0;
                        }
                        continue;
                    }
                    for(int j = Square_X; j < Cmax - BallDiameter + 1; j++){

                        if(*(Speed + j) >= 1){

                            *(Speed + j) += 1;

                            if(*(Speed + j) == BallDiameter){

                                *(Speed + j) = 0;
                            }
                        }
                    }
                    Square_X = Cmax - BallDiameter;
                }
            }
            else{

                if(*(Speed + Square_X) >= 1){

                    *(Speed +Square_X) += 1;
                }
                if(*(Speed + Square_X) == BallDiameter){

                    *(Speed + Square_X) = 0;
                }
            }
            
            // Updating each ball score if it is higher than the previous one and greater than BallminScore
            
            if(RedScore > (*RedBall).Score && RedScore > BallminScore){

                (*RedBall).Score = RedScore;
                (*RedBall).X = Square_X;
                (*RedBall).Y = Square_Y;
            }
            if(YellowScore > (*YellowBall).Score && YellowScore > BallminScore){

                (*YellowBall).Score = YellowScore;
                (*YellowBall).X = Square_X;
                (*YellowBall).Y = Square_Y;
            }
            if(WhiteScore > (*WhiteBall).Score && WhiteScore > BallminScore){

                (*WhiteBall).Score = WhiteScore;
                (*WhiteBall).X = Square_X;
                (*WhiteBall).Y = Square_Y;
            }
        }
    }

    free(Speed);
}

/**

Error codes:

    return 1: error in arguments (BallDiameter, Width, Height, number of arguments)
    return 2: error with Pixmap.bin file (opening, reading, closing)
    return 3: error with Pos.txt file (opening, reading, writing, closing)
    return 4: error with memory allocation
    return 0: exit at the end of Pix2Pos.c

*/