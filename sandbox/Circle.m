#import "Circle.h"
#import "Shape_c.h"

@implementation Circle
{
  const void* obj_;
}

- (id)init
{
  self = [super init];
  if (self)
  {
    obj_ = nil;
  }
  return self;
}

- (id)initWithRadius:(double)radius
{
  self = [super init];
  if (self)
  {
    obj_ = Shape_Circle_create(radius);
  }
  return self;
}

- (double)area;
{
  if ( obj_ ) return Shape_area(obj_);
  return 0.0;
}

- (double)perimeter;
{
  if ( obj_ ) return Shape_perimeter(obj_);
  return 0.0;
}

@end
