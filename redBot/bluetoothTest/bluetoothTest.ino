#include <RedBot.h>

#define BUF_SIZE  20
#define BAUD_RATE 9600

static RedBotSoftwareSerial swsp;



static void clearBuf(char *buf)
{
  for(int i =0; i < BUF_SIZE; i++)
  {
    buf[i] = '\0';
  }
}

//read in string of text from bluetooth module
static char* readInBuf()
{
  static char buf[BUF_SIZE];
  int bufInd = 0;
   
  clearBuf(buf);
    
  char c;
  while( (c = swsp.read()) != -1 )
  {
    buf[bufInd] = 'a';//c;
    bufInd = (bufInd + 1) % BUF_SIZE;
  }

  return buf;
}


void setup() {
 
  Serial.begin(BAUD_RATE);
  //Serial for bluetooth
  swsp.begin(BAUD_RATE);
}



void loop() {
  delay(500);

  char * buf;
  
  if( (buf = readInBuf())[0] != 0 )
  {
    Serial.println(buf);
  }
}
