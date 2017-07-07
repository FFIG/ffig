#include "ffig/attributes.h"

struct FFIG_EXPORT Asset
{
  virtual double PV() const = 0;
  virtual const char* name() const = 0;
  virtual ~Asset() = default;
};

struct CDO : Asset
{
  CDO() {}

  double PV() const override { return 0.0; }
  const char* name() const override { return "CDO"; }
};

