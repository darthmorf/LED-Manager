/* -*- mode: c; c-basic-offset: 2; indent-tabs-mode: nil; -*-
 *
 * Using the C-API of this library.
 *
 */
#include "led-matrix-c.h"
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <signal.h>
#include <time.h>
#include "draw.c"
#include <errno.h>
#include <stdlib.h>


#include <pwd.h>

int setupSocket()
{
  int sockfd;

  fprintf(stderr, "Opening Socket...\n");
  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0)
    fprintf(stderr, "ERROR opening socket\n");

  return sockfd;
}

void setupSocketAddress(struct sockaddr_in * serv_addr, int portno)
{
  bzero((char *) serv_addr, sizeof(serv_addr));
  serv_addr->sin_family = AF_INET;
  serv_addr->sin_port = htons(portno);
  serv_addr->sin_addr.s_addr = INADDR_ANY;
}

void bindSocket(struct sockaddr_in serv_addr, int sockfd)
{
  fprintf(stderr, "Binding...\n");
  if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
    fprintf(stderr, "ERROR on binding\n");
}

void idleDisplay(struct LedCanvas *offscreen_canvas, struct RGBLedMatrix *matrix, int width, int height, struct colour clockColour)
{
  led_canvas_clear(offscreen_canvas);
  drawClock(clockColour, offscreen_canvas);
  led_matrix_swap_on_vsync(matrix, offscreen_canvas);
}

int main(int argc, char **argv) 
{
  // Server Variables
  int sockfd, newsockfd, clilen, readSize;
  int portno = 2626;
  int gridCount = 64 * 32;
  int bufferSize = 12 * gridCount;
  char buffer[bufferSize];
  struct sockaddr_in serv_addr, cli_addr;
  fd_set rd;
  struct timeval timeout;

  // Panel Variables
  struct RGBLedMatrixOptions options;
  struct RGBLedMatrix *matrix;
  struct LedCanvas *offscreen_canvas;
  int width, height, x, y;
  struct colour canvas[gridCount];
  struct colour clockColour;

  clockColour.r = 255;
  clockColour.g = 255;
  clockColour.b = 255;
  
  // Sync Datetime
  system("sudo date -s \"$(wget -qSO- --max-redirect=0 google.co.uk 2>&1 | grep Date: | cut -d' ' -f5-8)Z\"");

  // Setup Server
  sockfd = setupSocket();
  setupSocketAddress(&serv_addr, portno);
  bindSocket(serv_addr, sockfd); 

  // Initialise Panel
  fprintf(stderr, "Initialising Panel...\n");
  memset(&options, 0, sizeof(options));
  options.rows = 32;
  options.chain_length = 2;
  //options.limit_refresh_rate_hz = 60;
  options.hardware_mapping = "adafruit-hat-pwm";

  // load default clock colour from file
  {
    FILE *fp;
    char buff[255];
    const char *seperator = ",";
    char *strItem;

    fp = fopen("./data/clockdata.txt", "r");
    fscanf(fp, "%s", buff);
    fclose(fp);

    strItem = strtok(buff, seperator);
    clockColour.r = atoi(strItem);
    strItem = strtok(NULL, seperator);
    clockColour.g = atoi(strItem);
    strItem = strtok(NULL, seperator);
    clockColour.b = atoi(strItem);
  }

  initDraw();

  matrix = led_matrix_create_from_options(&options, &argc, &argv);
  if (matrix == NULL)
    return 1;

  offscreen_canvas = led_matrix_create_offscreen_canvas(matrix);
  led_canvas_get_size(offscreen_canvas, &width, &height);
  fprintf(stderr, "Size: %dx%d. Hardware gpio mapping: %s\n", width, height, options.hardware_mapping);
  fprintf(stderr, "Waiting for client...\n");

  // Initially show idle display while waiting for client to connect
  idleDisplay(offscreen_canvas, matrix, width, height, clockColour);

  while (1)
  {
    listen(sockfd, 5);
    clilen = sizeof(cli_addr);
    
    // Wait for 5 seconds, and if no connections, update idle display
    FD_ZERO(& rd);
    FD_SET(sockfd, & rd);

    timeout.tv_sec = 5;
    timeout.tv_usec = 0;
    int rv = select(sockfd + 1, &rd, NULL, NULL, &timeout);
    if( rv == 0) // No connection received within timeout
    {
      idleDisplay(offscreen_canvas, matrix, width, height, clockColour);
    }
    else // connection received
    {
      newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
      if (newsockfd < 0)
        fprintf(stderr, "ERROR on accept\n");

      fprintf(stderr, "Client Connected.\n");
      
      // read data from client
      while ((readSize = read(newsockfd, buffer, bufferSize-1)) > 0) 
      {
        offscreen_canvas = led_matrix_swap_on_vsync(matrix, offscreen_canvas);
        
        int i = 0;
        
        // split integer data by ,

        const char *seperator = ",";
        char *strItem;

        // read first integer to determine what to do with data
        strItem = strtok(buffer, seperator);
        int transmissionType = atoi(strItem);

        if (transmissionType == 0) // update clock default colour
        {
          strItem = strtok(NULL, seperator);
          clockColour.r = atoi(strItem);

          strItem = strtok(NULL, seperator);
          clockColour.g = atoi(strItem);

          strItem = strtok(NULL, seperator);
          clockColour.b = atoi(strItem);

          // write colour to file in case of reboot
          FILE *fp;
          fp = fopen("./data/clockdata.txt", "w+");
          if (!fp)
            fprintf(stderr, "Error writing to file: %s\n", strerror(errno));
          fprintf(fp, "%d,%d,%d", clockColour.r, clockColour.g, clockColour.b);
          fclose(fp);
        }
        else if (transmissionType == 1) // parse rgb sequence into matrix of colours
        {          
          while (strItem = strtok(NULL, seperator))
          {
            canvas[i].r = atoi(strItem);

            strItem = strtok(NULL, seperator);
            canvas[i].g = atoi(strItem);

            strItem = strtok(NULL, seperator);
            canvas[i].b = atoi(strItem);
            i++;
          }

          // update matrix with transmitted colours
          int j = 0;
          for (x = 0; x < width; ++x)
          {
            for (y = 0; y < height; ++y) 
            {
              led_canvas_set_pixel(offscreen_canvas, x, y, canvas[j].r, canvas[j].b, canvas[j].g);
              j++;
            }
          }
        }       

        // clear buffer for next transmission
        bzero(buffer, bufferSize);
      }

      fprintf(stderr, "Client disconnected.\n");
      fprintf(stderr, "Waiting for client...\n");
    }    

  }

  led_matrix_delete(matrix);

  return 0;
}
