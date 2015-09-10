import sys
sys.path.insert(0,'/usr/local/Cellar/llvm36/3.6.2/lib/python2.7/site-packages/clang-3.6')
import clang.cindex
if not clang.cindex.Config.library_file:
  clang.cindex.Config.set_library_file('/usr/local//Cellar/llvm36/3.6.2/lib/llvm-3.6/lib/libclang.dylib')

def _get_annotations(node):
  return [c.displayname for c in node.get_children()
      if c.kind == clang.cindex.CursorKind.ANNOTATE_ATTR]

class Field:
  def __repr__(self):
    return str(self.type)+":\""+str(self.name)+"\""

  def __init__(self,cursor):
    self.name = cursor.spelling
    self.type = cursor.type.spelling


class FunctionArgument:
  def __repr__(self):
    return str(self.type)+":\""+str(self.name)+"\""

  def __init__(self, type, name):
    self.type = type
    self.name = name


class Function(object):
  def __repr__(self):
    return "Function:"+str(self.name)

  def __init__(self, cursor):
    self.function_cursor = cursor
    self.name = cursor.spelling
    arguments = [x.spelling for x in cursor.get_arguments()]
    argument_types = [x.spelling for x in cursor.type.argument_types()]
    self.type = cursor.type.spelling
    self.return_type = cursor.type.get_result().spelling
    self.annotations = _get_annotations(cursor)
    
    self.arguments = [FunctionArgument(t,n) for (t,n) in zip(argument_types,arguments)]


class Class(object):
  def __repr__(self):
    return "Class:%s"%str(self.name)

  def __init__(self, cursor):
    self.name = cursor.spelling
    self.functions = []
    self.fields = []
    self.annotations = _get_annotations(cursor)
    self.base_classes = []

    for c in cursor.get_children():
      if (c.kind == clang.cindex.CursorKind.FIELD_DECL):
        m = Field(c)
        self.fields.append(m)
      elif (c.kind == clang.cindex.CursorKind.CXX_METHOD):
        f = Function(c)
        self.functions.append(f)
      elif (c.kind == clang.cindex.CursorKind.CONSTRUCTOR):
        f = Function(c)
        self.functions.append(f)
      elif (c.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER):
        self.base_classes.append(c.type.spelling)

    self.constructors = [x for x in self.functions if x.name == self.name]


def build_classes(cursor):
  result = []
  for c in cursor.get_children():
    if c.kind == clang.cindex.CursorKind.CLASS_DECL:
      a_class = Class(c)
      result.append(a_class)
    elif c.kind == clang.cindex.CursorKind.STRUCT_DECL:
      a_class = Class(c)
      result.append(a_class)
    elif c.kind == clang.cindex.CursorKind.NAMESPACE:
      child_classes = build_classes(c)
      result.extend(child_classes)

  return result


def parse_classes(class_file):
  index = clang.cindex.Index.create()
  translation_unit = index.parse(class_file, ['-x', 'c++', '-std=c++14'])
  classes = build_classes(translation_unit.cursor)
  return classes

