
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

   char **digit = bigDigits[value];
   
    for (int i = 0; i < bigDigitHeight; i++)
    {
        for (int j = 0; j < 10; j++)
        {
            if(digit[i][j] == '1')
                led_canvas_set_pixel(offscreen_canvas, x+j, y+i, drawColour.r, drawColour.g, drawColour.b);
        }
    }
    
}

void clockColon(struct colour drawColour, struct LedCanvas *offscreen_canvas)
{
    led_canvas_set_pixel(offscreen_canvas, 31, 6,  drawColour.r, drawColour.g, drawColour.b);
    led_canvas_set_pixel(offscreen_canvas, 32, 6,  drawColour.r, drawColour.g, drawColour.b);
    led_canvas_set_pixel(offscreen_canvas, 31, 7,  drawColour.r, drawColour.g, drawColour.b);
    led_canvas_set_pixel(offscreen_canvas, 32, 7,  drawColour.r, drawColour.g, drawColour.b);
    led_canvas_set_pixel(offscreen_canvas, 31, 8,  drawColour.r, drawColour.g, drawColour.b);
    led_canvas_set_pixel(offscreen_canvas, 32, 8,  drawColour.r, drawColour.g, drawColour.b);

    led_canvas_set_pixel(offscreen_canvas, 31, 15, drawColour.r, drawColour.g, drawColour.b);
    led_canvas_set_pixel(offscreen_canvas, 32, 15, drawColour.r, drawColour.g, drawColour.b);
    led_canvas_set_pixel(offscreen_canvas, 31, 16, drawColour.r, drawColour.g, drawColour.b);
    led_canvas_set_pixel(offscreen_canvas, 32, 16, drawColour.r, drawColour.g, drawColour.b);
    led_canvas_set_pixel(offscreen_canvas, 31, 17, drawColour.r, drawColour.g, drawColour.b);
    led_canvas_set_pixel(offscreen_canvas, 32, 17, drawColour.r, drawColour.g, drawColour.b);
}

int weekday(struct colour drawColour, struct LedCanvas *offscreen_canvas, int weekdayIndex)
{
    int x = 3;
    int y = 22;

    char **weekday = days[weekdayIndex];

    for (int i = 0; i < dayHeight; i++)
    {
        for (int j = 0; j < dayWidths[weekdayIndex]; j++)
        {
            if(weekday[i][j] == '1')
                led_canvas_set_pixel(offscreen_canvas, x+j, y+i, drawColour.r, drawColour.g, drawColour.b);
        }
    }

    return dayWidths[weekdayIndex];
}

int date(struct colour drawColour, struct LedCanvas *offscreen_canvas, int dayWidth, int value)
{
    int x = dayWidth + 6;
    int y = 23;

    char **digit = smallDigits[value];

    for (int i = 0; i < smallDigitHeight; i++)
    {
        for (int j = 0; j < smallDigitWidths[value]; j++)
        {
            if(digit[i][j] == '1')
                led_canvas_set_pixel(offscreen_canvas, x+j, y+i, drawColour.r, drawColour.g, drawColour.b);
        }
    }

    return smallDigitWidths[value];
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

    char timeBuffer[50];
    sprintf(timeBuffer, "%d%d", tm->tm_hour, tm->tm_min);

    clockDigit(0, timeBuffer[0] - '0', drawColour, offscreen_canvas);
    clockDigit(1, timeBuffer[1] - '0', drawColour, offscreen_canvas);
    clockDigit(2, timeBuffer[2] - '0', drawColour, offscreen_canvas);
    clockDigit(3, timeBuffer[3] - '0', drawColour, offscreen_canvas);

    clockColon(drawColour, offscreen_canvas);

    int dayWidth = weekday(drawColour, offscreen_canvas, tm->tm_wday);

    int dateWidth;

    if (tm->tm_mday < 10)
    {
        dateWidth = date(drawColour, offscreen_canvas, dayWidth, tm->tm_mday);
    }
    else
    {
        sprintf(timeBuffer, "%d", tm->tm_mday);

        dateWidth = date(drawColour, offscreen_canvas, dayWidth, timeBuffer[0] - '0');
        dateWidth += date(drawColour, offscreen_canvas, dayWidth+dateWidth+1, timeBuffer[1] - '0');
    }

    
}


