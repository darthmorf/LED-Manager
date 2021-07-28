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

struct colour {
  int r;
  int g;
  int b;
};

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

int main(int argc, char **argv) 
{
  // Server Variables
  int sockfd, newsockfd, clilen, n;
  int portno = 2626;
  int gridCount = 64 * 32;
  int bufferSize = 12 * gridCount;
  char buffer[bufferSize];
  struct sockaddr_in serv_addr, cli_addr;

  // Panel Variables
  struct RGBLedMatrixOptions options;
  struct RGBLedMatrix *matrix;
  struct LedCanvas *offscreen_canvas;
  int width, height, x, y;
  struct colour canvas[gridCount];
  

  // Setup Server
  sockfd = setupSocket();
  setupSocketAddress(&serv_addr, portno);
  bindSocket(serv_addr, sockfd); 

  fprintf(stderr, "Waiting for client...\n");
  listen(sockfd, 5);
  clilen = sizeof(cli_addr);
  newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
  if (newsockfd < 0)
    fprintf(stderr, "ERROR on accept\n");


  // Initialise Panel
  fprintf(stderr, "Initialising Panel...\n");
  memset(&options, 0, sizeof(options));
  options.rows = 32;
  options.chain_length = 2;
  //options.limit_refresh_rate_hz = 60;
  options.hardware_mapping = "adafruit-hat-pwm";

  matrix = led_matrix_create_from_options(&options, &argc, &argv);
  if (matrix == NULL)
    return 1;

  offscreen_canvas = led_matrix_create_offscreen_canvas(matrix);

  led_canvas_get_size(offscreen_canvas, &width, &height);

  fprintf(stderr, "Size: %dx%d. Hardware gpio mapping: %s\n", width, height, options.hardware_mapping);

  while (1) 
  {
    offscreen_canvas = led_matrix_swap_on_vsync(matrix, offscreen_canvas);
    
  
    bzero(buffer, bufferSize);
    n = read(newsockfd, buffer, bufferSize-1);

    int i = 0;

    if (n > 0) 
    {
      const char *seperator = ",";
      char *rgbItem;

      rgbItem = strtok(buffer, seperator);
      canvas[i].r = atoi(rgbItem);

      rgbItem = strtok(NULL, seperator);
      canvas[i].g = atoi(rgbItem);

      rgbItem = strtok(NULL, seperator);
      canvas[i].b = atoi(rgbItem);
      i++;

      while (rgbItem = strtok(NULL, seperator))
      {
        canvas[i].r = atoi(rgbItem);

        rgbItem = strtok(NULL, seperator);
        canvas[i].g = atoi(rgbItem);

        rgbItem = strtok(NULL, seperator);
        canvas[i].b = atoi(rgbItem);
        i++;
      }

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
  }

  led_matrix_delete(matrix);

  return 0;
}
