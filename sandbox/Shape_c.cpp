#include <new>
#include "Shape_c.h"
#include "Shape.h"

#define RC_SUCCESS 0
#define RC_FAIL 1

static thread_local std::string Shape_error_;

void Shape_clear_error()
{
  Shape_error_.clear();
}

const char* Shape_error()
{
  if ( ! Shape_error_.empty() )
  {
    return Shape_error_.str();
  }
}

void Shape_dispose(const void* myShape, int* rc)
{
  delete reinterpret_cast<const Shape*>(myShape);
}

double Shape_area(const void* myShape)
{
  try 
  {
    return reinterpret_cast<const Shape*>(myShape)->area();
  }
  catch(const std::exception& e)
  {
    Shape_error_ = e.what();
    *rc = RC_FAIL;
  }
  *rc = RC_SUCCESS;
}

double Shape_perimeter(const void* myShape)
{
  return reinterpret_cast<const Shape*>(myShape)->perimeter();
}

const char* Shape_name(const void* myShape)
{
  return reinterpret_cast<const Shape*>(myShape)->name();
}

bool Shape_is_equal(const void* myShape, const void* s)
{
  return reinterpret_cast<const Shape*>(myShape)->is_equal((const Shape *)s);
}

const void* Shape_Circle_create(double radius)
{
  return new (std::nothrow) Circle(radius);
}

const void* Shape_Square_create(double side)
{
  return new (std::nothrow) Square(side);
}

const void* Shape_Pentagon_create(double side)
{
  return new (std::nothrow) Pentagon(side);
}

