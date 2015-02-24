#include <cmath>

#define C_API __attribute__((annotate("GENERATE_C_API")))

struct Shape
{
  virtual ~Shape() {}
  virtual double area() const = 0;
  virtual double perimeter() const = 0;
  virtual const char* name() const = 0;
} C_API;

static const double pi = 3.14159265359;

class Circle : public Shape
{
  const double radius_;

public:
  double area() const override { return pi * radius_ * radius_; }

  double perimeter() const override { return 2 * pi * radius_; }
  
  const char* name() const override { return "Circle"; }

  Circle(double r) : radius_(r) {}
};

class Square : public Shape
{
  const double side_;

public:
  double area() const override { return side_ * side_; }

  double perimeter() const override { return 4.0 * side_; }
  
  const char* name() const override { return "Square"; }

  Square(double s) : side_(s) {}
};

class Pentagon : public Shape
{
  const double side_;

public:
  double area() const override { return 0.25 * sqrt(5.*(5.+2.*sqrt(5.))) * side_ * side_; }

  double perimeter() const override { return 5.0 * side_; }
  
  const char* name() const override { return "Pentagon"; }

  Pentagon(double s) : side_(s) {}
};
