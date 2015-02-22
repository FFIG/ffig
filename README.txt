Usage (prints generated source to standard output)

./generate.py Shapes.h h.tmpl
./generate.py Shapes.h cpp.tmpl

clang++ -shared -Wl,-install_name,testlib.so -o testlib.so -fPIC testlib.c
