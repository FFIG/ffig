#import <Foundation/Foundation.h>
#import "Circle.h"

int main(int argc, const char * argv[]) {
  double r = argc > 1 ? atoi(argv[1]) : 4.0;

  Circle* circle = [[Circle alloc] initWithRadius:r];
  printf("Circle with radius %f has perimeter %.2f and area %.2f\n", r, [circle perimeter], [circle area]);
  return 0;
}
