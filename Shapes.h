
#define C_API __attribute__((annotate("GENERATE_C_API")))

struct Shape
{
  virtual ~Shape() {}
  virtual double area(double r) const = 0;
  virtual double perimeter(double r) const = 0;
} C_API;

static const double pi = 3.14159265359;

class Circle : public Shape
{
  const double radius_;

public:
  double area() const override { return pi * radius_ * radius_; }

  double perimeter() const override { return 2 * pi * radius_; }

  Circle(double r) : radius_(r) {}
};

class Square : public Shape
{
  const double side_;

public:
  double area() const override { return side_ * side_; }

  double perimeter() const override { return 4.0 * side_; }

  Square(double s) : side_(s) {}
};