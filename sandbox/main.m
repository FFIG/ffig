#import <Foundation/Foundation.h>
#import "Circle.h"

int main(int argc, const char * argv[]) {
  double r = argc > 1 ? atoi(argv[1]) : 4.0;

  Circle* circle = [[Circle alloc] initWithRadius:r];
  printf("%s with radius %.0f has perimeter %.2f and area %.2f\n",
         [[circle name] UTF8String], r, [circle perimeter], [circle area]);
  return 0;
}
