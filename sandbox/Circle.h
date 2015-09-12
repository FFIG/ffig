#import <Foundation/Foundation.h>

@interface Circle : NSObject
{
}

- (id)init;

- (id)initWithRadius:(double)radius;

- (void)dealloc;

- (double)area;

- (double)perimeter;

- (NSString*)name;

@end
