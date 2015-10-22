#include <cmath>

// Any class annotated with this macro will be exposed and have all functions
// exposed.
// Any class deriving from an exposed class will have its constructors exposed.
#define C_API __attribute__((annotate("GENERATE_C_API")))

enum class ShapeKind
{
  Circle,
  Square,
  Pentagon
};

struct ShapeBase
{
  virtual ShapeKind kind() const = 0;
};

struct Shape : ShapeBase
{
  virtual ~Shape()
  {
  }
  virtual double area() const = 0;
  virtual double perimeter() const = 0;
  virtual const char* name() const = 0;
  virtual bool is_equal(const Shape* s) const = 0;
} C_API;

static const double pi = 3.14159265359;

class Circle : public Shape
{
  const double radius_;

public:
  double area() const override
  {
    return pi * radius_ * radius_;
  }

  double perimeter() const override
  {
    return 2 * pi * radius_;
  }

  const char* name() const override
  {
    return "Circle";
  }

  bool is_equal(const Shape* s) const override
  {
    if (s->kind() != kind()) return false;
    auto c = static_cast<const Circle*>(s);
    return c->radius_ == radius_;
  }

  Circle(double radius) : radius_(radius)
  {
  }

  ShapeKind kind() const override final
  {
    return ShapeKind::Circle;
  }
};

class Square : public Shape
{
  const double side_;

public:
  double area() const override
  {
    return side_ * side_;
  }

  double perimeter() const override
  {
    return 4.0 * side_;
  }

  const char* name() const override
  {
    return "Square";
  }

  bool is_equal(const Shape* s) const override
  {
    if (s->kind() != kind()) return false;
    auto sq = static_cast<const Square*>(s);
    return sq->side_ == side_;
  }

  Square(double side) : side_(side)
  {
  }

  ShapeKind kind() const override final
  {
    return ShapeKind::Square;
  }
};

class Pentagon : public Shape
{
  const double side_;

public:
  double area() const override
  {
    return 0.25 * sqrt(5. * (5. + 2. * sqrt(5.))) * side_ * side_;
  }

  double perimeter() const override
  {
    return 5.0 * side_;
  }

  const char* name() const override
  {
    return "Pentagon";
  }

  bool is_equal(const Shape* s) const override
  {
    if (s->kind() != kind()) return false;
    auto p = static_cast<const Pentagon*>(s);
    return p->side_ == side_;
  }

  Pentagon(double side) : side_(side)
  {
  }

  ShapeKind kind() const override final
  {
    return ShapeKind::Pentagon;
  }
};
