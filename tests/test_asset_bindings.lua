require("Asset")

assert(Asset_error() == "")

a = CDO:new()

assert(a:name() == "CDO")

assert(a:value() == 99.99)

