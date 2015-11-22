from ctypes import *
c_object_p = POINTER(c_void_p)

class Shape:
  
  def area(self):
    rv = c_double()
    rc = conf.lib.Shape_area(self,byref(rv))
    if rc != 0:
      raise Exception("Failed to evalaute area of Shape")
    return rv.value

  def perimeter(self):
    return conf.lib.Shape_perimeter(self)
    
  def name(self):
    return conf.lib.Shape_name(self)
    
  def is_equal(self, s ):
    return conf.lib.Shape_is_equal(self, s)
    
  def from_param(self):
    return self.ptr

  def __del__(self):
    conf.lib.Shape_dispose(self)

class Circle(Shape): 
  def __init__(self, radius):
    self.ptr = c_object_p()
    rc = conf.lib.Shape_Circle_create(radius,byref(self.ptr))
    if rc != 0:
        raise Exception("Failed to create Circle with radius {}".format(radius))
 
class Square(Shape): 
  def __init__(self, side):
    self.ptr=conf.lib.Shape_Square_create(side)
 
class Pentagon(Shape): 
  def __init__(self, side):
    self.ptr=conf.lib.Shape_Pentagon_create(side)
 


methodList = [

  ("Shape_dispose",
  [Shape],
  None), 
  
  ("Shape_Circle_create",
  [c_double, POINTER(c_object_p)],
  c_int), 
  
  ("Shape_Square_create",
  [c_double],
  c_object_p), 
  
  ("Shape_Pentagon_create",
  [c_double],
  c_object_p), 
  
  ("Shape_area",
  [Shape, POINTER(c_double)],
  c_int),
  
  ("Shape_perimeter",
  [Shape],
  c_double),
  
  ("Shape_name",
  [Shape],
  c_char_p),
  
  ("Shape_is_equal",
  [Shape, Shape  ],
  bool)
]

# library loading and method registrations
# based on clang python bindings approach

def register_method(lib, item):
  func = getattr(lib, item[0])

  if len(item) >= 2:
    func.argtypes = item[1]

  if len(item) >= 3:
    func.restype = item[2]


class CachedProperty(object):

    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except:
            pass

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        value = self.wrapped(instance)
        setattr(instance, self.wrapped.__name__, value)

        return value

class Config:
    library_path = None
    loaded = False

    @staticmethod
    def set_library_path(path):
        if Config.loaded:
            raise Exception("library path is already set.")
        Config.library_path = path

    @CachedProperty
    def lib(self):
        lib = self._get_library()
        map(lambda x:register_method(lib,x), methodList)
        Config.loaded = True
        return lib

    def _get_filename(self):
        import platform
        name = platform.system()

        if name == 'Darwin':
            file = 'libShape_c.dylib'
        elif name == 'Windows':
            file = 'Shape_c.dll'
        else:
            file = 'libShape_c.so'

        if Config.library_path:
            file = Config.library_path + '/' + file

        return file

    def _get_library(self):
        try:
            library = cdll.LoadLibrary(self._get_filename())
        except OSError as e:
            msg = str(e) + ". To provide a path to Shape dylib use Config.set_library_path()"
            raise Exception(msg)

        return library  

conf = Config()


