require 'ffi'

class Foo
  attr_reader :bar
  def initialize(n)
    @bar = n
    ObjectSpace.define_finalizer( self, self.class.finalize(bar) )
  end

  def self.finalize(bar)
    proc { puts "DESTROY OBJECT #{bar}" }
  end

end


f=Foo.new(101)
puts "Foo.bar is #{f.bar} now"
f=nil

# Force ruby to start the Garbage Collector
# In a real program you don't have to do this
# ruby will run the GC automatically.
GC.start
sleep 1 # make sure you will see the message
        # before ruby quits
puts "done"


module Shape
  extend FFI::Library
  ffi_lib 'Shape_c'
  attach_function :Shape_error, [], :string
  attach_function :Shape_clear_error, [], :void
  attach_function :Shape_Circle_create, [:double, :pointer], :int
  attach_function :Shape_area, [:pointer, :pointer], :int 
  attach_function :Shape_perimeter, [:pointer, :pointer], :int 
  attach_function :Shape_name, [:pointer, :pointer], :int 
  attach_function :Shape_dispose, [:pointer], :void
end

objptr = FFI::MemoryPointer.new :pointer
c = Shape.Shape_Circle_create(10, objptr)
objptr = objptr.get_pointer(0)

dptr = FFI::MemoryPointer.new :double
Shape.Shape_perimeter(objptr, dptr)
puts "Perimeter is #{dptr.get_double(0)}"

dptr = FFI::MemoryPointer.new :double
Shape.Shape_area(objptr, dptr)
puts "Area is #{dptr.get_double(0)}"

Shape.Shape_dispose(objptr)

Shape.Shape_Circle_create(-10, objptr)
puts "Error is #{Shape.Shape_error}"
Shape.Shape_clear_error()

