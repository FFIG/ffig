#include <new>
#include "Shape_c.h"
#include "Shape.h"
 #include <new>

void Shape_dispose(const void* myShape)
{
  delete reinterpret_cast<const Shape*>(myShape);
}

double Shape_area(const void* myShape)
{
  return reinterpret_cast<const Shape*>(myShape)->area();
}

double Shape_perimeter(const void* myShape)
{
  return reinterpret_cast<const Shape*>(myShape)->perimeter();
}

const char* Shape_name(const void* myShape)
{
  return reinterpret_cast<const Shape*>(myShape)->name();
}

void Shape_Dummy(const void* myShape, const void * s)
{
  return reinterpret_cast<const Shape*>(myShape)->Dummy((const Shape *)s);
}
  
const void* Shape_Circle_create(double r)
{
  return new (std::nothrow) Circle(r);
}
  
const void* Shape_Square_create(double s)
{
  return new (std::nothrow) Square(s);
}
  
const void* Shape_Pentagon_create(double s)
{
  return new (std::nothrow) Pentagon(s);
}
 

