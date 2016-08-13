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

