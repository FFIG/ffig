from ctypes import *
c_object_p = POINTER(c_void_p)

class Shape:
  
  def area(self):
    return conf.lib.Shape_area(self)
    
  def perimeter(self):
    return conf.lib.Shape_perimeter(self)
    
  def name(self):
    return conf.lib.Shape_name(self)
    
  def from_param(self):
    return self.ptr

  def __del__(self):
    conf.lib.Shape_dispose(self)

class Circle(Shape): 
  def __init__(self, r):
    self.ptr=conf.lib.Shape_Circle_create(r)
 
class Square(Shape): 
  def __init__(self, s):
    self.ptr=conf.lib.Shape_Square_create(s)
 
class Pentagon(Shape): 
  def __init__(self, s):
    self.ptr=conf.lib.Shape_Pentagon_create(s)
 


functionList = [

  ("Shape_dispose",
  [Shape],
  None), 
  
  ("Shape_Circle_create",
  [c_double],
  c_object_p), 
  
  ("Shape_Square_create",
  [c_double],
  c_object_p), 
  
  ("Shape_Pentagon_create",
  [c_double],
  c_object_p), 
  
  ("Shape_area",
  [Shape],
  c_double),
  
  ("Shape_perimeter",
  [Shape],
  c_double),
  
  ("Shape_name",
  [Shape],
  c_char_p)
]

# library loading and function registrations
# based on clang python bindings approach

def register_function(lib, item):
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
        map(lambda x:register_function(lib,x), functionList)
        Config.loaded = True
        return lib

    def _get_filename(self):
        import platform
        name = platform.system()

        if name == 'Darwin':
            file = 'Shape_c.dylib'
        elif name == 'Windows':
            file = 'Shape_c.dll'
        else:
            file = 'Shape_c.so'

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


