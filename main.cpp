#include "HUB75driver.h"

//Initialisation:
HUB75driver matrix;
//if first argument is true double buffering used, need swapBuffers() to refresh
//if second argument is true additional dimming will be applyed. brightness will reduce by half
matrix.init(true, true);
matrix.begin();//Enable interupt
//Drawing
matrix.cleanScreen();//Clean screen
matrix.drawPixel(1, 1, 1, 0, 0);//put single point. parameters x,y,r,g,b
matrix.swapBuffers();//must be used if double buffering enabled