#import <Foundation/Foundation.h>
#import "Circle.h"

int main(int argc, const char * argv[]) {
  double r = 4.0;
  Circle* circle = [[Circle alloc] initWithRadius:4.0];
  printf("Circle with radius %f has perimeter %f and area %f\n", r, [circle perimeter], [circle area]);
  return 0;
}
