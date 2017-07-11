#include "ffig/attributes.h"

struct FFIG_EXPORT Asset
{
  virtual FFIG_EXPORT_NAME(value) double PV() const = 0;
  virtual FFIG_PROPERTY_NAME(name) const char* id() const = 0;
  virtual ~Asset() = default;
};

struct FFIG_NAME(CDO) CollateralisedDebtObligation : Asset
{
  CollateralisedDebtObligation() {}

  double PV() const override { return 0.0; }
  const char* id() const override { return "CDO"; }
};

