
#include <stdio.h>

#define bigDigitHeight 18
#define dayHeight 9
#define smallDigitHeight 7

char **bigDigits[10];
char *big0[bigDigitHeight];
char *big1[bigDigitHeight];
char *big2[bigDigitHeight];
char *big3[bigDigitHeight];
char *big4[bigDigitHeight];
char *big5[bigDigitHeight];
char *big6[bigDigitHeight];
char *big7[bigDigitHeight];
char *big8[bigDigitHeight];
char *big9[bigDigitHeight];

char **days[7];
char *monday[dayHeight];
char *tuesday[dayHeight];
char *wednesday[dayHeight];
char *thursday[dayHeight];
char *friday[dayHeight];
char *saturday[dayHeight];
char *sunday[dayHeight];
int dayWidths[] = { 27, 28, 34, 47, 38, 24, 37 };

char **smallDigits[10];
char *small0[smallDigitHeight];
char *small1[smallDigitHeight];
char *small2[smallDigitHeight];
char *small3[smallDigitHeight];
char *small4[smallDigitHeight];
char *small5[smallDigitHeight];
char *small6[smallDigitHeight];
char *small7[smallDigitHeight];
char *small8[smallDigitHeight];
char *small9[smallDigitHeight];
int smallDigitWidths[] = { 5, 2, 5, 4, 5, 4, 4, 4, 4 };



void setupChars()
{
    big0[ 0] = "  111111  " ;
    big0[ 1] = " 11111111 " ;
    big0[ 2] = "111   1111" ;
    big0[ 3] = "11    1111" ;
    big0[ 4] = "11   11111" ;
    big0[ 5] = "11   11 11" ;
    big0[ 6] = "11   11 11" ;
    big0[ 7] = "11  111 11" ;
    big0[ 8] = "11  11  11" ;
    big0[ 9] = "11  11  11" ;
    big0[10] = "11 111  11" ;
    big0[11] = "11 11   11" ;
    big0[12] = "11 11   11" ;
    big0[13] = "11111   11" ;
    big0[14] = "1111    11" ;
    big0[15] = "1111   111" ;
    big0[16] = " 11111111 " ;
    big0[17] = "  111111  " ;

    big1[ 0] = "      1   " ;
    big1[ 1] = "     11   " ;
    big1[ 2] = "    111   " ;
    big1[ 3] = "   1111   " ;
    big1[ 4] = "  11 11   " ;
    big1[ 5] = " 11  11   " ;
    big1[ 6] = " 1   11   " ;
    big1[ 7] = "     11   " ;
    big1[ 8] = "     11   " ;
    big1[ 9] = "     11   " ;
    big1[10] = "     11   " ;
    big1[11] = "     11   " ;
    big1[12] = "     11   " ;
    big1[13] = "     11   " ;
    big1[14] = "     11   " ;
    big1[15] = "     11   " ;
    big1[16] = "  11111111" ;
    big1[17] = "  11111111" ;

    big2[ 0] = "  111111  " ;
    big2[ 1] = " 11111111 " ;
    big2[ 2] = "111    111" ;
    big2[ 3] = "11      11" ;
    big2[ 4] = "1       11" ;
    big2[ 5] = "        11" ;
    big2[ 6] = "        11" ;
    big2[ 7] = "       111" ;
    big2[ 8] = "      111 " ;
    big2[ 9] = "     111  " ;
    big2[10] = "    111   " ;
    big2[11] = "   111    " ;
    big2[12] = "  111     " ;
    big2[13] = " 111      " ;
    big2[14] = "111       " ;
    big2[15] = "11        " ;
    big2[16] = "1111111111" ;
    big2[17] = "1111111111" ;

    big3[ 0] = "  111111  " ;
    big3[ 1] = " 11111111 " ;
    big3[ 2] = "111    111" ;
    big3[ 3] = "11      11" ;
    big3[ 4] = "1       11" ;
    big3[ 5] = "       111" ;
    big3[ 6] = "      111 " ;
    big3[ 7] = "    1111  " ;
    big3[ 8] = "    1111  " ;
    big3[ 9] = "      111 " ;
    big3[10] = "       111" ;
    big3[11] = "        11" ;
    big3[12] = "        11" ;
    big3[13] = "1       11" ;
    big3[14] = "11      11" ;
    big3[15] = "111    111" ;
    big3[16] = " 11111111 " ;
    big3[17] = "  111111  " ;

    big4[ 0] = "     111  " ;
    big4[ 1] = "     111  " ;
    big4[ 2] = "    1111  " ;
    big4[ 3] = "    1111  " ;
    big4[ 4] = "   11 11  " ;
    big4[ 5] = "   11 11  " ;
    big4[ 6] = "  11  11  " ;
    big4[ 7] = "  11  11  " ;
    big4[ 8] = " 11   11  " ;
    big4[ 9] = " 11   11  " ;
    big4[10] = "11    11  " ;
    big4[11] = "11    11  " ;
    big4[12] = "1111111111" ;
    big4[13] = "1111111111" ;
    big4[14] = "      11  " ;
    big4[15] = "      11  " ;
    big4[16] = "      11  " ;
    big4[17] = "      11  " ;

    big5[ 0] = "1111111111" ;
    big5[ 1] = "1111111111" ;
    big5[ 2] = "11        " ;
    big5[ 3] = "11        " ;
    big5[ 4] = "11        " ;
    big5[ 5] = "11        " ;
    big5[ 6] = "11 11111  " ;
    big5[ 7] = "111111111 " ;
    big5[ 8] = "111    111" ;
    big5[ 9] = "        11" ;
    big5[10] = "        11" ;
    big5[11] = "        11" ;
    big5[12] = "        11" ;
    big5[13] = "        11" ;
    big5[14] = "11      11" ;
    big5[15] = "111    111" ;
    big5[16] = " 11111111 " ;
    big5[17] = "  111111  " ;

    big6[ 0] = "   11111  " ;
    big6[ 1] = "  1111111 " ;
    big6[ 2] = " 111   111" ;
    big6[ 3] = "111     11" ;
    big6[ 4] = "11      11" ;
    big6[ 5] = "11        " ;
    big6[ 6] = "11        " ;
    big6[ 7] = "11        " ;
    big6[ 8] = "11 11111  " ;
    big6[ 9] = "111111111 " ;
    big6[10] = "111    111" ;
    big6[11] = "11      11" ;
    big6[12] = "11      11" ;
    big6[13] = "11      11" ;
    big6[14] = "11      11" ;
    big6[15] = "111    111" ;
    big6[16] = " 11111111 " ;
    big6[17] = "  111111  " ;

    big7[ 0] = "1111111111" ;
    big7[ 1] = "1111111111" ;
    big7[ 2] = "        11" ;
    big7[ 3] = "        11" ;
    big7[ 4] = "       111" ;
    big7[ 5] = "       11 " ;
    big7[ 6] = "      111 " ;
    big7[ 7] = "     111  " ;
    big7[ 8] = "     11   " ;
    big7[ 9] = "     11   " ;
    big7[10] = "    111   " ;
    big7[11] = "    11    " ;
    big7[12] = "    11    " ;
    big7[13] = "   111    " ;
    big7[14] = "   11     " ;
    big7[15] = "   11     " ;
    big7[16] = "   11     " ;
    big7[17] = "   11     " ;

    big8[ 0] = "  111111  " ;
    big8[ 1] = " 11111111 " ;
    big8[ 2] = "111    111" ;
    big8[ 3] = "11      11" ;
    big8[ 4] = "11      11" ;
    big8[ 5] = "11      11" ;
    big8[ 6] = "111    111" ;
    big8[ 7] = " 11111111 " ;
    big8[ 8] = "  111111  " ;
    big8[ 9] = " 11111111 " ;
    big8[10] = "111    111" ;
    big8[11] = "11      11" ;
    big8[12] = "11      11" ;
    big8[13] = "11      11" ;
    big8[14] = "11      11" ;
    big8[15] = "111    111" ;
    big8[16] = " 11111111 " ;
    big8[17] = "  111111  " ;

    big9[ 0] = "  111111  " ;
    big9[ 1] = " 11111111 " ;
    big9[ 2] = "111    111" ;
    big9[ 3] = "11      11" ;
    big9[ 4] = "11      11" ;
    big9[ 5] = "11      11" ;
    big9[ 6] = "11      11" ;
    big9[ 7] = "11      11" ;
    big9[ 8] = "111    111" ;
    big9[ 9] = " 111111111" ;
    big9[10] = "  11111111" ;
    big9[11] = "       111" ;
    big9[12] = "        11" ;
    big9[13] = "        11" ;
    big9[14] = "1       11" ;
    big9[15] = "11     111" ;
    big9[16] = "111111111 " ;
    big9[17] = " 1111111  " ;

    bigDigits[0] = big0;
    bigDigits[1] = big1;
    bigDigits[2] = big2;
    bigDigits[3] = big3;
    bigDigits[4] = big4;
    bigDigits[5] = big5;
    bigDigits[6] = big6;
    bigDigits[7] = big7;
    bigDigits[8] = big8;
    bigDigits[9] = big9;


    monday[0] = "1   1             1          ";
    monday[1] = "1   1             1          ";
    monday[2] = "11 11  11  11   111  11  1 1 ";
    monday[3] = "11 11 1  1 1 1 1  1    1 1 1 ";
    monday[4] = "1 1 1 1  1 1 1 1  1   11 1 1 ";
    monday[5] = "1 1 1 1  1 1 1 1  1  1 1  11 ";
    monday[6] = "1 1 1  11  1 1  11 1 11 1  1 ";
    monday[7] = "                           1 ";
    monday[8] = "                         11  ";

   tuesday[0] = "11111                   1          ";
   tuesday[1] = "  1                     1          ";
   tuesday[2] = "  1  1 1   11   1111  111  11  1 1 ";
   tuesday[3] = "  1  1 1  1  1 1     1  1    1 1 1 ";
   tuesday[4] = "  1  1 1  1111  111  1  1   11 1 1 ";
   tuesday[5] = "  1  1 1  1        1 1  1  1 1  11 ";
   tuesday[6] = "  1   1 1  111 1111   11 1 11 1  1 ";
   tuesday[7] = "                                 1 ";
   tuesday[8] = "                               11  ";

    wednesday[0] = "1     1         1                    1         ";
    wednesday[1] = "1     1         1                    1         ";
    wednesday[2] = "1  1  1  11   111  11   11   1111  111  11  1 1";
    wednesday[3] = " 1 1 1  1  1 1  1  1 1 1  1 1     1  1    1 1 1";
    wednesday[4] = " 1 1 1  1111 1  1  1 1 1111  111  1  1   11 1 1";
    wednesday[5] = "  1 1   1    1  1  1 1 1        1 1  1  1 1  11";
    wednesday[6] = "  1 1    111  11 1 1 1  111 1111   11 1 11 1  1";
    wednesday[7] = "                                              1";
    wednesday[8] = "                                            11 ";

    thursday[0] = "11111 1                     1         ";
    thursday[1] = "  1   1                     1         ";
    thursday[2] = "  1   11  1 1 1 1   1111  111  11  1 1";
    thursday[3] = "  1   1 1 1 1  1 1 1     1  1    1 1 1";
    thursday[4] = "  1   1 1 1 1  1    111  1  1   11 1 1";
    thursday[5] = "  1   1 1 1 1  1       1 1  1  1 1  11";
    thursday[6] = "  1   1 1 11 1 1   1111   11 1 11 1  1";
    thursday[7] = "                                     1";
    thursday[8] = "                                   11 ";

    friday[0] = "1111          1         ";
    friday[1] = "1             1         ";
    friday[2] = "1   1 1  1  111  11  1 1";
    friday[3] = "111  1 1   1  1    1 1 1";
    friday[4] = "1    1   1 1  1   11 1 1";
    friday[5] = "1    1   1 1  1  1 1  11";
    friday[6] = "1    1   1  11 1 11 1  1";
    friday[7] = "                       1";
    friday[8] = "                     11 ";

    saturday[0] = " 11                        1         ";
    saturday[1] = "1  1       1               1         ";
    saturday[2] = "1    11   111 1 1  1 1   111  11  1 1";
    saturday[3] = " 11    1   1  1 1   1 1 1  1    1 1 1";
    saturday[4] = "   1  11   1  1 1   1   1  1   11 1 1";
    saturday[5] = "1  1 1 1   1  1 1   1   1  1  1 1  11";
    saturday[6] = " 11  11 1  11  1 1  1    11 1 11 1  1";
    saturday[7] = "                                    1";
    saturday[8] = "                                  11 ";

    sunday[0] =  " 11              1         ";
    sunday[1] =  "1  1             1         ";
    sunday[2] =  "1    1 1  11   111  11  1 1";
    sunday[3] =  " 11  1 1  1 1 1  1    1 1 1";
    sunday[4] =  "   1 1 1  1 1 1  1   11 1 1";
    sunday[5] =  "1  1 1 1  1 1 1  1  1 1  11";
    sunday[6] =  " 11   1 1 1 1  11 1 11 1  1";
    sunday[7] =  "                          1";
    sunday[8] =  "                        11 ";

    days[0] = sunday;
    days[1] = monday;
    days[2] = tuesday;
    days[3] = wednesday;
    days[4] = thursday;
    days[5] = friday;
    days[6] = saturday;


    small0[0] = " 111 " ;
    small0[1] = "1   1" ;
    small0[2] = "1   1" ;
    small0[3] = "1   1" ;
    small0[4] = "1   1" ;
    small0[5] = "1   1" ;
    small0[6] = " 111 " ;

    small1[0] = " 1" ;
    small1[1] = "11" ;
    small1[2] = " 1" ;
    small1[3] = " 1" ;
    small1[4] = " 1" ;
    small1[5] = " 1" ;
    small1[6] = " 1" ;
    
    small2[0] = " 11" ;
    small2[1] = "1  1" ;
    small2[2] = "   1" ;
    small2[3] = "  1 " ;
    small2[4] = " 1  " ;
    small2[5] = "1   " ;
    small2[6] = "1111" ;
    
    small3[0] = "111 " ;
    small3[1] = "   1" ;
    small3[2] = "   1" ;
    small3[3] = " 11 " ;
    small3[4] = "   1" ;
    small3[5] = "   1" ;
    small3[6] = "111 " ;
    
    small4[0] = "  11 " ;
    small4[1] = " 1 1 " ;
    small4[2] = " 1 1 " ;
    small4[3] = "1  1 " ;
    small4[4] = "11111" ;
    small4[5] = "   1 " ;
    small4[6] = "   1 " ;
    
    small5[0] = "1111" ;
    small5[1] = "1   " ;
    small5[2] = "1   " ;
    small5[3] = "111 " ;
    small5[4] = "   1" ;
    small5[5] = "1  1" ;
    small5[6] = " 11 " ;
    
    small6[0] = " 11 " ;
    small6[1] = "1  1" ;
    small6[2] = "1   " ;
    small6[3] = "111 " ;
    small6[4] = "1  1" ;
    small6[5] = "1  1" ;
    small6[6] = " 11 " ;
    
    small7[0] = "1111" ;
    small7[1] = "   1" ;
    small7[2] = "   1" ;
    small7[3] = "  1 " ;
    small7[4] = "  1 " ;
    small7[5] = " 1  " ;
    small7[6] = " 1  " ;
    
    small8[0] = " 11 " ;
    small8[1] = "1  1" ;
    small8[2] = "1  1" ;
    small8[3] = " 11 " ;
    small8[4] = "1  1" ;
    small8[5] = "1  1" ;
    small8[6] = " 11 " ;
    
    small9[0] = " 11 " ;
    small9[1] = "1  1" ;
    small9[2] = "1  1" ;
    small9[3] = " 111" ;
    small9[4] = "   1" ;
    small9[5] = "1  1" ;
    small9[6] = " 11 " ;

    smallDigits[0] = small0;
    smallDigits[1] = small1;
    smallDigits[2] = small2;
    smallDigits[3] = small3;
    smallDigits[4] = small4;
    smallDigits[5] = small5;
    smallDigits[6] = small6;
    smallDigits[7] = small7;
    smallDigits[8] = small8;
    smallDigits[9] = small9;
}
