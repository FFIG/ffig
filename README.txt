Usage (prints generated source to standard output)

./generate.py Shapes.h h.tmpl
./generate.py Shapes.h cpp.tmpl

clang++ -std=c++11 -shared -Wl, -o shape.dylib -fPIC c_shape.cpp
clang++ -std=c++11 -shared -Wl, -o shape.dylib -fPIC c_shape.cpp
