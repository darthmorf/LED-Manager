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


int main(int argc, char **argv) 
{
  // Panel Variables
  struct RGBLedMatrixOptions options;
  struct RGBLedMatrix *matrix;
  struct LedCanvas *offscreen_canvas;
  int width, height, x, y;
  int r = 255, g = 255, b = 255;

  // Server Variables
  int sockfd, newsockfd, portno, clilen, n;
  char buffer[256];
  struct sockaddr_in serv_addr, cli_addr;
  

  // Setup Server
  fprintf(stderr, "Opening Socket...\n");
  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0)
    fprintf(stderr, "ERROR opening socket");

  bzero((char *) &serv_addr, sizeof(serv_addr));
  portno = 2626;
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(portno);
  serv_addr.sin_addr.s_addr = INADDR_ANY;

  fprintf(stderr, "Binding...\n");
  if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
    fprintf(stderr, "ERROR on binding");

  fprintf(stderr, "Waiting for client...\n");
  listen(sockfd, 5);
  clilen = sizeof(cli_addr);
  newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
  if (newsockfd < 0)
    fprintf(stderr, "ERROR on accept");


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

  while (1 == 1) 
  {
     for (y = 0; y < height; ++y) 
     {
      for (x = 0; x < width; ++x) 
      {
        led_canvas_set_pixel(offscreen_canvas, x, y, r, g, b);        
      }
    }

    offscreen_canvas = led_matrix_swap_on_vsync(matrix, offscreen_canvas);
    
    bzero(buffer, 256);
    n = read(newsockfd, buffer, 255);

    if (n > 0) 
    {
	    fprintf(stderr, "%s\n", buffer);

      char *token = strtok(buffer, ",");
      r = atoi(token);
      token = strtok(NULL, ",");
      g = atoi(token);
      token = strtok(NULL, ",");
      b = atoi(token);
	    fprintf(stderr, "RGB: %d,%d,%d\n", r, g, b);
    }
  }

  led_matrix_delete(matrix);

  return 0;
}
