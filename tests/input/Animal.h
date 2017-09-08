#include "ffig/attributes.h"

class FFIG_EXPORT Cat
{
public:
  Cat() = default;

  const char* noise() const
  {
    return "Miaow";
  }
};

class FFIG_EXPORT Duck
{
public:
  Duck() = default;

  const char* noise() const
  {
    return "Quack";
  }
};

class FFIG_EXPORT Squirrel
{
public:
  Squirrel() = default;

  const char* noise() const
  {
    return "<deafening silence>";
  }
};

