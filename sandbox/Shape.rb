require 'ffi'

module Shape_c
  extend FFI::Library
  ffi_lib 'Shape_c'
  attach_function :Shape_error, [], :string
  attach_function :Shape_clear_error, [], :void
  attach_function :Shape_Circle_create, [:double, :pointer], :int
  attach_function :Shape_Pentagon_create, [:double, :pointer], :int
  attach_function :Shape_Square_create, [:double, :pointer], :int
  attach_function :Shape_area, [:pointer, :pointer], :int 
  attach_function :Shape_perimeter, [:pointer, :pointer], :int 
  attach_function :Shape_name, [:pointer, :pointer], :int 
  attach_function :Shape_dispose, [:pointer], :void
end

class Shape
  def initialize(objptr)
    @ptr = objptr.get_pointer(0)
    ObjectSpace.define_finalizer( self, self.class.finalize(@ptr) )
  end
  
  def area()
    dptr = FFI::MemoryPointer.new :double
    Shape_c.Shape_area(@ptr, dptr)
    dptr.get_double(0)
  end
  
  def perimeter()
    dptr = FFI::MemoryPointer.new :double
    Shape_c.Shape_perimeter(@ptr, dptr)
    dptr.get_double(0)
  end

  def name()
    dptr = FFI::MemoryPointer.new(:pointer, 1)
    Shape_c.Shape_name(@ptr, dptr)
    strPtr = dptr.read_pointer()
    return strPtr.null? ? nil : strPtr.read_string()
  end

  def self.finalize(ptr)
    proc { Shape_c.Shape_dispose(ptr) }
  end
end

class ShapeError < Exception
  def initialize()
    msg = Shape_c.Shape_error
    Shape_c.Shape_clear_error()
    super(msg)
  end
end

class Circle < Shape
  def initialize(x)
    objptr = FFI::MemoryPointer.new :pointer
    rc = Shape_c.Shape_Circle_create(x, objptr)
    if rc != 0
      raise ShapeError
    end
    super(objptr)
  end
end

class Pentagon < Shape
  def initialize(x)
    objptr = FFI::MemoryPointer.new :pointer
    rc = Shape_c.Shape_Pentagon_create(x, objptr)
    if rc != 0
      raise ShapeError
    end
    super(objptr)
  end
end

class Square < Shape
  def initialize(x)
    objptr = FFI::MemoryPointer.new :pointer
    rc = Shape_c.Shape_Square_create(x, objptr)
    if rc != 0
      raise ShapeError
    end
    super(objptr)
  end
end

# r = 8
# c = Circle.new(8)
# puts "Radius = #{r}"
# puts "Perimeter = #{c.perimeter}"
# puts "Area = #{c.area}"
# 
# # Force ruby to start the Garbage Collector
# # In a real program you don't have to do this
# # ruby will run the GC automatically.
# c = nil
# 
# c = Circle.new(-10)
# 
# GC.start
# sleep 1 # make sure you will see the message
#         # before ruby quits
# puts "Done"
