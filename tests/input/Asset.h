#include "ffig/attributes.h"

struct FFIG_EXPORT Asset
{
  virtual FFIG_EXPORT_NAME(value) double PV() const = 0;
  virtual FFIG_EXPORT_NAME(name) const char* id() const = 0;
  virtual ~Asset() = default;
};

struct CDO : Asset
{
  CDO() {}

  double PV() const override { return 0.0; }
  const char* id() const override { return "CDO"; }
};

