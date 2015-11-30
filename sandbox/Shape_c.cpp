#include <new>
#include <memory>
#include <atomic>
#include "Shape_c.h"
#include "Shape.h"

namespace {
  
struct Shape_block
{
  std::shared_ptr<const Shape> object_;
  Shape_block(const Shape_block&) = delete;
  
  Shape_block() = default;

  template<typename T, typename ...Ts>
  static Shape_block* create(Ts&&...ts)
  {
    auto block = std::make_unique<Shape_block>();
    block->object_ = std::make_shared<T>(std::forward<Ts>(ts)...);
    return block.release();
  }

  template<typename T>
  static Shape_block* create_subobject(const T* parent, const Shape* object)
  {
    auto block = std::make_unique<Shape_block>();
    //use aliasing constructor of shared_ptr to keep parent alive
    block->object_ = std::shared_ptr<T>(parent, object);
    return block.release();
  }
};

}

void Shape_dispose(const void* myShape)
{
  auto block = reinterpret_cast<const Shape_block*>(myShape);
  delete block;
}

/*
const void* Shape_component(const void* myShape, int i)
{
  auto block = reinterpret_cast<const Shape_block*>(myShape);
  return Shape_block::create_subobject(block, block->object_->component(i));
}

double Shape_component_count(const void* myShape)
{
  auto block = reinterpret_cast<const Shape_block*>(myShape);
  return block->object_->component_count();
}
*/

double Shape_area(const void* myShape)
{
  auto block = reinterpret_cast<const Shape_block*>(myShape);
  return block->object_->area();
}

double Shape_perimeter(const void* myShape)
{
  auto block = reinterpret_cast<const Shape_block*>(myShape);
  return block->object_->perimeter();
}

const char* Shape_name(const void* myShape)
{
  auto block = reinterpret_cast<const Shape_block*>(myShape);
  return block->object_->name();
}

bool Shape_is_equal(const void* myShape, const void* s)
{
  auto block = reinterpret_cast<const Shape_block*>(myShape);
  auto arg_block = reinterpret_cast<const Shape_block*>(s);
  return block->object_->is_equal(arg_block->object_.get());
}

const void* Shape_Circle_create(double radius)
{
  return Shape_block::create<Circle>(radius);
}
  
const void* Shape_Square_create(double side)
{
  return Shape_block::create<Square>(side);
}
  
const void* Shape_Pentagon_create(double side)
{
  return Shape_block::create<Pentagon>(side);
}
 
