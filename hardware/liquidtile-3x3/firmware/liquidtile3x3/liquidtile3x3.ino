/*
    Basic Pin setup:
    ------------                                  ---u----
    ARDUINO   13|-> SCLK (pin 25)           OUT1 |1     28| OUT channel 0
              12|                           OUT2 |2     27|-> GND (VPRG)
              11|-> SIN (pin 26)            OUT3 |3     26|-> SIN (pin 11)
              10|-> BLANK (pin 23)          OUT4 |4     25|-> SCLK (pin 13)
               9|-> XLAT (pin 24)             .  |5     24|-> XLAT (pin 9)
               8|                             .  |6     23|-> BLANK (pin 10)
               7|                             .  |7     22|-> GND
               6|                             .  |8     21|-> VCC (+5V)
               5|                             .  |9     20|-> 2K Resistor -> GND
               4|                             .  |10    19|-> +5V (DCPRG)
               3|-> GSCLK (pin 18)            .  |11    18|-> GSCLK (pin 3)
               2|                             .  |12    17|-> SOUT
               1|                             .  |13    16|-> XERR
               0|                           OUT14|14    15| OUT channel 15
    ------------                                  --------

    -  Put the longer leg (anode) of the LEDs in the +5V and the shorter leg
         (cathode) in OUT(0-15).
    -  +5V from Arduino -> TLC pin 21 and 19     (VCC and DCPRG)
    -  GND from Arduino -> TLC pin 22 and 27     (GND and VPRG)
    -  digital 3        -> TLC pin 18            (GSCLK)
    -  digital 9        -> TLC pin 24            (XLAT)
    -  digital 10       -> TLC pin 23            (BLANK)
    -  digital 11       -> TLC pin 26            (SIN)
    -  digital 13       -> TLC pin 25            (SCLK)
    -  The 2K resistor between TLC pin 20 and GND will let ~20mA through each
       LED.  To be precise, it's I = 39.06 / R (in ohms).  This doesn't depend
       on the LED driving voltage.
    - (Optional): put a pull-up resistor (~10k) between +5V and BLANK so that
                  all the LEDs will turn off when the Arduino is reset.

    If you are daisy-chaining more than one TLC, connect the SOUT of the first
    TLC to the SIN of the next.  All the other pins should just be connected
    together:
        BLANK on Arduino -> BLANK of TLC1 -> BLANK of TLC2 -> ...
        XLAT on Arduino  -> XLAT of TLC1  -> XLAT of TLC2  -> ...
    The one exception is that each TLC needs it's own resistor between pin 20
    and GND.

    This library uses the PWM output ability of digital pins 3, 9, 10, and 11.
    Do not use analogWrite(...) on these pins.

    Alex Leone <acleone ~AT~ gmail.com>, 2009-02-03 for the TLC code
    Christopher Woodall for the serial communications code
    */

#include "Tlc5940.h"

#include <avr/interrupt.h>
#include <avr/io.h>

enum tile_uart_states {
  IDLE,
  PIXEL_ADDRESS,
  GET_COLOR,
  END
};

// {R, G, B}
static uint8_t pixel_mapping[9][3] = {
  {1, 2, 0},
  {4, 5, 3},
  {7,8,6},
  {10, 11, 9},
  {13,14,12},
  {17,18,16},
  {20,21,19},
  {23,24,22},
  {26,27,25}
};
void setPixel(uint8_t pixel, uint8_t r, uint8_t g, uint8_t b) {
  if (pixel < 9) {
    Tlc.set(pixel_mapping[pixel][0],r<<4);
    Tlc.set(pixel_mapping[pixel][1],g<<4);
    Tlc.set(pixel_mapping[pixel][2],b<<4);
  }
}
void setup()
{
  /* Call Tlc.init() to setup the tlc.
     You can optionally pass an initial PWM value (0 - 4095) for all channels.*/
  Tlc.init();
  // Initialize Timer 0 (NOTE WE CANT USE ARDUINO DELAYS ANY MORE
 /* cli();
  // We want a 100Hz refresh rate
  // 16 MHz/1024 = 15.625kHz <-- Prescaler = CS2[2:0] = 0b101 
  // This is the slowest we can run the timer. But don't worry we can interrupt on counts within this
   // Now we want to set the counter so we update near 100Hz.
  // 15.625kHz / 100Hz = 156.25 ~= 156 counts   
  OCR0A = 156;
  TCCR0B = (1<< WGM02) | (1<<CS02) | (1<<CS00); // Turn on CTC mode.
  TCCR0A = 0;

  TIMSK0 = (1<<OCIE0A);
  sei(); */
  Serial.begin(19200);
}


/* This loop will create a Knight Rider-like effect if you have LEDs plugged
   into all the TLC outputs.  NUM_TLCS is defined in "tlc_config.h" in the
   library folder.  After editing tlc_config.h for your setup, delete the
   Tlc5940.o file to save the changes. */

static enum tile_uart_states uart_state = IDLE;
static uint8_t counter = 0;
static uint8_t color_counter = 0;
static uint8_t address = 0;
static uint8_t rgb[3] = {0,0,0};
#define START_CHAR ':'

void loop()
{
  char new_char;
  char *end_ptr;
  char *scratch_pad = "\0\0"; //Start off with 3 null terminators
  uint8_t dump = 0;

//  int direction = 1;
  if (Serial.available()) {
    new_char = Serial.read();
    scratch_pad = "\0\0";
    //Serial.write(new_char);
    if (new_char == '\n') {
      color_counter = 0;
      counter = 0;
      uart_state = IDLE;
    } else {
      switch (uart_state) {
        case IDLE:    
          color_counter = 0;
          counter = 0;
          if (new_char == START_CHAR) {
            uart_state = PIXEL_ADDRESS;
          }
          break;
        case PIXEL_ADDRESS:
          if (new_char == 'u') {
            Tlc.update();
          } else {
            scratch_pad[0] = new_char;
            scratch_pad[1] = '\0';
            address = strtol(scratch_pad, &end_ptr, 16);
            if (!*end_ptr) {
              uart_state = GET_COLOR;
            } else {
              uart_state = IDLE;
            }
          }
          break;
        case GET_COLOR:
          if (counter == 0) {
            scratch_pad[0] = new_char;
            counter += 1;
          } else {
            scratch_pad[1] = new_char;
            rgb[color_counter] = strtol(scratch_pad, &end_ptr, 16);
            if (color_counter == 2) {
              uart_state = IDLE;
              setPixel(address, rgb[0], rgb[1], rgb[2]);
            } else {
               color_counter += 1;
            }
            counter = 0;
          }
          break;
      }
    }
  }
  //      Tlc.set(channel, 4095);
}

/*ISR(TIMER0_COMPA_vect) {
    Tlc.update(); // Update the display.
}*/
