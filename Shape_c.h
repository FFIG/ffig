
#pragma once

extern "C" void Shape_dispose(const void* myShape);

extern "C" double Shape_area(const void* myShape);

extern "C" double Shape_perimeter(const void* myShape);

extern "C" const char* Shape_name(const void* myShape);

extern "C" void Shape_Dummy(const void* myShape, const void * s);
  
extern "C" const void* Shape_Circle_create(double r);
  
extern "C" const void* Shape_Square_create(double s);
  
extern "C" const void* Shape_Pentagon_create(double s);
 

