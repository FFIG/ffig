require("Shape")

assert(SHape_error() == "")

c = Circle:new(8)

assert(c:name() == "Circle")

assert(c:area() == 3.14159 * 8 * 8)

