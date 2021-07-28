
#include <stdio.h>
#include "chars.c"
#include "led-matrix-c.h"

struct colour {
  int r;
  int g;
  int b;
};

void initDraw()
{
    setupChars();
}

void clockDigit(int index, int value, struct colour drawColour, struct LedCanvas *offscreen_canvas)
{
    int x = 0;
    int y = 3;

    if (index == 0)
        x = 3;
    else if (index == 1)
        x = 3 + 10 + 4;
    else if (index == 2)
        x = 3 + 10 + 4 + 10 + 10;
    else
        x = 3 + 10 + 4 + 10 + 10 + 10 + 4;

    char *digit = big0;

    for (int i = 0; i < 18; i++)
    {
        for (int j = 0; j < 10; j++)
        {
            if(big0[i][j] == '1')
                led_canvas_set_pixel(offscreen_canvas, x+j, y+i, drawColour.r, drawColour.g, drawColour.b);
        }
    }
    
}

void drawClock(struct colour drawColour, struct LedCanvas *offscreen_canvas)
{
    time_t now;
    struct tm *tm;
    now = time(0);

    if ((tm = localtime (&now)) == NULL) 
    {
        fprintf(stderr, "Error extracting time stuff\n");
        return;
    }

    int hours = tm->tm_hour;
    int minutes = tm->tm_min;

    clockDigit(0, 6, drawColour, offscreen_canvas);
    clockDigit(1, 9, drawColour, offscreen_canvas);
    clockDigit(2, 2, drawColour, offscreen_canvas);
    clockDigit(3, 4, drawColour, offscreen_canvas);
}


