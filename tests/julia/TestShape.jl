using Base.Test

include("../../build_out/generated/Shape.jl")
using FFIG

@test area(Square(3.0)) == 9.0

@test perimeter(Square(3.0)) == 12.0

@test name(Circle(3.0)) == "Circle"
