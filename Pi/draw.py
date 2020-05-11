#!/usr/bin/env python
from datetime import datetime


def clock(color, grid):

    time = datetime.now().strftime("%H%M")

    for i in range(len(time)):
        clockDigit(i,int(time[i]), color, grid)

    grid.setPixel(31, 6, color)
    grid.setPixel(32, 6, color)
    grid.setPixel(31, 7, color)
    grid.setPixel(32, 7, color)
    grid.setPixel(31, 8, color)
    grid.setPixel(32, 8, color)

    grid.setPixel(31, 15, color)
    grid.setPixel(32, 15, color)
    grid.setPixel(31, 16, color)
    grid.setPixel(32, 16, color)
    grid.setPixel(31, 17, color)
    grid.setPixel(32, 17, color)


def clockDigit(index, value, color, grid):
    x = 0
    y = 3

    if index == 0:
        x = 3
    elif index == 1:
        x = 3 + 10 + 4
    elif index == 2:
        x = 3 + 10 + 4 + 10 + 10
    else:
        x = 3 + 10 + 4 + 10 + 10 + 10 + 4

    chars = [
                [
                    "  111111  ",
                    " 11111111 ",
                    "111   1111",
                    "11    1111",
                    "11   11111",
                    "11   11 11",
                    "11   11 11",
                    "11  111 11",
                    "11  11  11",
                    "11  11  11",
                    "11 111  11",
                    "11 11   11",
                    "11 11   11",
                    "11111   11",
                    "1111    11",
                    "1111   111",
                    " 11111111 ",
                    "  111111  "
                ],
                [
                    "      1   ",
                    "     11   ",
                    "    111   ",
                    "   1111   ",
                    "  11 11   ",
                    " 11  11   ",
                    "11   11   ",
                    "     11   ",
                    "     11   ",
                    "     11   ",
                    "     11   ",
                    "     11   ",
                    "     11   ",
                    "     11   ",
                    "     11   ",
                    "     11   ",
                    "     11   ",
                    "     11   "
                ],
                [
                    "  111111  ",
                    " 11111111 ",
                    "111    111",
                    "11      11",
                    "1       11",
                    "        11",
                    "        11",
                    "       111",
                    "      111 ",
                    "     111  ",
                    "    111   ",
                    "   111    ",
                    "  111     ",
                    " 111      ",
                    "111       ",
                    "11        ",
                    "1111111111",
                    "1111111111"
                ],
                [
                    "  111111  ",
                    " 11111111 ",
                    "111    111",
                    "11      11",
                    "1       11",
                    "       111",
                    "      111 ",
                    "    1111  ",
                    "    1111  ",
                    "      111 ",
                    "       111",
                    "        11",
                    "        11",
                    "1       11",
                    "11      11",
                    "111    111",
                    " 11111111 ",
                    "  111111  "
                ],
                [
                    "     111  ",
                    "     111  ",
                    "    1111  ",
                    "    1111  ",
                    "   11 11  ",
                    "   11 11  ",
                    "  11  11  ",
                    "  11  11  ",
                    " 11   11  ",
                    " 11   11  ",
                    "11    11  ",
                    "11    11  ",
                    "1111111111",
                    "1111111111",
                    "      11  ",
                    "      11  ",
                    "      11  ",
                    "      11  "
                ],
                [
                    "1111111111",
                    "1111111111",
                    "11        ",
                    "11        ",
                    "11        ",
                    "11        ",
                    "11 11111  ",
                    "111111111 ",
                    "111    111",
                    "        11",
                    "        11",
                    "        11",
                    "        11",
                    "        11",
                    "11      11",
                    "111    111",
                    " 11111111 ",
                    "  111111  "
                ],
                [
                    "   11111  ",
                    "  1111111 ",
                    " 111   111",
                    "111     11",
                    "11      11",
                    "11        ",
                    "11        ",
                    "11        ",
                    "11 11111  ",
                    "111111111 ",
                    "111    111",
                    "11      11",
                    "11      11",
                    "11      11",
                    "11      11",
                    "111    111",
                    " 11111111 ",
                    "  111111  "
                ],
                [
                    "1111111111",
                    "1111111111",
                    "        11",
                    "        11",
                    "       111",
                    "       11 ",
                    "      111 ",
                    "     111  ",
                    "     11   ",
                    "     11   ",
                    "    111   ",
                    "    11    ",
                    "    11    ",
                    "   111    ",
                    "   11     ",
                    "   11     ",
                    "   11     ",
                    "   11     "
                ],
                [
                    "  111111  ",
                    " 11111111 ",
                    "111    111",
                    "11      11",
                    "11      11",
                    "11      11",
                    "111    111",
                    " 11111111 ",
                    "  111111  ",
                    " 11111111 ",
                    "111    111",
                    "11      11",
                    "11      11",
                    "11      11",
                    "11      11",
                    "111    111",
                    " 11111111 ",
                    "  111111  "
                ],
                [
                    "  111111  ",
                    " 11111111 ",
                    "111    111",
                    "11      11",
                    "11      11",
                    "11      11",
                    "11      11",
                    "11      11",
                    "111    111",
                    " 111111111",
                    "  11111111",
                    "       111",
                    "        11",
                    "        11",
                    "1       11",
                    "11     111",
                    "111111111 ",
                    " 1111111  "
                ]
            ]

    char = chars[value]

    for i in range(len(char)):
        for j in range(len(char[i])):
            if char[i][j] == "1":
                grid.setPixel(x+j, y+i, color)


def clockDay(color, grid):
    x = 1
    y = 22
    
    value = datetime.now().weekday()

    days = [
        [
            "       1   1             1         ",
            "       1   1             1         ",
            "       11 11  11  11   111  11  1 1",
            "       11 11 1  1 1 1 1  1    1 1 1",
            "       1 1 1 1  1 1 1 1  1   11 1 1",
            "       1 1 1 1  1 1 1 1  1  1 1  1 ",
            "       1 1 1  11  1 1  11 1 11 1 1 ",
            "                                 1 ",
            "                               11  " 
        ],
        [
          "      11111                   1         ",
          "        1                     1         ",
          "        1  1 1   11   1111  111  11  1 1",
          "        1  1 1  1  1 1     1  1    1 1 1",
          "        1  1 1  1111  11   1  1   11 1 1",
          "        1  1 1  1       1  1  1  1 1  1 ",
          "        1   1 1  111 111    11 1 11 1 1 ",
          "                                      1 ",
          "                                    11  " 
        ],
        [
            "1     1         1                    1         ",
            "1     1         1                    1         ",
            "1  1  1  11   111  11   11   1111  111  11  1 1",
            " 1 1 1  1  1 1  1  1 1 1  1 1     1  1    1 1 1",
            " 1 1 1  1111 1  1  1 1 1111  11   1  1   11 1 1",
            "  1 1   1    1  1  1 1 1       1  1  1  1 1  1 ",
            "  1 1    111  11 1 1 1  111 111    11 1 11 1 1 ",
            "                                             1 ",
            "                                           11  "
        ],
        [
            "    11111 1                     1         ",
            "      1   1                     1         ",
            "      1   11  1 1 1 1   1111  111  11  1 1",
            "      1   1 1 1 1  1 1 1     1  1    1 1 1",
            "      1   1 1 1 1  1    111  1  1   11 1 1",
            "      1   1 1 1 1  1       1 1  1  1 1  1 ",
            "      1   1 1 11 1 1   1111   11 1 11 1 1 ",
            "                                        1 ",
            "                                      11  "
        ],
        [
            "           1111          1         ",
            "           1             1         ",
            "           1   1 1  1  111  11  1 1",
            "           111  1 1   1  1    1 1 1",
            "           1    1   1 1  1   11 1 1",
            "           1    1   1 1  1  1 1  1 ",
            "           1    1   1  11 1 11 1 1 ",
            "                                 1 ",
            "                               11  "
        ],
        [
            "     11                        1         ",
            "    1  1       1               1         ",
            "    1    11   111 1 1  1 1   111  11  1 1",
            "     11    1   1  1 1   1 1 1  1    1 1 1",
            "       1  11   1  1 1   1   1  1   11 1 1",
            "    1  1 1 1   1  1 1   1   1  1  1 1  1 ",
            "     11  11 1  11  1 1  1    11 1 11 1 1 ",
            "                                       1 ",
            "                                     11  " 
        ],
        [      
            "            11              1         ",
            "           1  1             1         ",
            "           1    1 1  11   111  11  1 1",
            "            11  1 1  1 1 1  1    1 1 1",
            "              1 1 1  1 1 1  1   11 1 1",
            "           1  1 1 1  1 1 1  1  1 1  1 ",
            "            11   1 1 1 1  11 1 11 1 1 ",
            "                                    1 ",
            "                                  11  "
        ]
    ]

    day = days[value]
    for i in range(len(day)):
        for j in range(len(day[i])):
            if day[i][j] == "1":
                grid.setPixel(x+j, y+i, color)


    