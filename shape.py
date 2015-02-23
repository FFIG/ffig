from ctypes import *

lib = cdll.LoadLibrary("shape.dylib")

functionList = [
    ("Shape_Square_create",
    [c_double],
    c_void_p),
    ("Shape_Circle_create",
    [c_double],
    c_void_p),
    ("Shape_dispose",
    [c_void_p],
    None),
    ("Shape_area",
    [c_void_p],
    c_double),
    ("Shape_perimeter",
    [c_void_p],
    c_double),
    ]

def register_function(item):
  func = getattr(lib, item[0])

  if len(item) >= 2:
    func.argtypes = item[1]

  if len(item) >= 3:
    func.restype = item[2]

map(register_function, functionList)

class Shape:
  def area(self):
    return lib.Shape_area(self.ptr)

  def perimeter(self):
    return lib.Shape_perimeter(self.ptr)

  def __del__(self):
    lib.Shape_dispose(self.ptr)

class Square(Shape):
  def __init__(self,x):
    self.ptr = self._as_parameter_ = lib.Shape_Square_create(x)

class Circle(Shape):
  def __init__(self,x):
    self.ptr = self._as_parameter_ = lib.Shape_Circle_create(x)
