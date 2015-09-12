#import "Circle.h"

static const double my_pi = 3.14159265359;

@implementation Circle
{
  double radius_;
}

- (id)init
{
  self = [super init];
  if (self)
  {
    radius_ = 1.0;
  }
  return self;
}

- (id)initWithRadius:(double)radius
{
  self = [super init];
  if (self)
  {
    radius_ = radius;
  }
  return self;
}

- (double)area;
{
  return my_pi * radius_ * radius_;
}

- (double)perimeter;
{
  return 2.0 * my_pi * radius_;
}

@end
