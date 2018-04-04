#include "ffig/attributes.h"

class FFIG_EXPORT Number 
{
  int value_;

public:
  Number(int value) : value_(value)
  {
  }

  Number next() const {
    return Number(value_ + 1);
  }

  int value() const noexcept {
    return value_;
  }
};
