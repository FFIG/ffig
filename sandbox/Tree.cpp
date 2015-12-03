#include <memory>
#include <random>

static std::mt19937 mt;
static std::uniform_int_distribution<int> d(1,10);
static auto gen = []{return d(mt);};

class Tree
{
  int data_;
  std::shared_ptr<Tree> left_;
  std::shared_ptr<Tree> right_;

  public:

  Tree(int levels=0)
  {
    data_ = gen();
    if ( levels <= 0 ) return;
    left_ = std::make_shared<Tree>(levels-1);
    right_ = std::make_shared<Tree>(levels-1);
  }

  const Tree* left() const
  {
    return left_.get();
  }

  const Tree* right() const
  {
    return right_.get();
  }

  int data() const
  {
    return data_;
  }

};

////////////////////////////////////////////////////////////////////////////////

namespace {

  template <typename T>
  struct Block
  {
    std::shared_ptr<const T> object_;
    Block(const Block&) = delete;

    Block() = default;

    template<typename ...Ts>
      static Block* create(Ts&&...ts)
      {
        auto block = std::make_unique<Block>();
        block->object_ = std::make_shared<T>(std::forward<Ts>(ts)...);
        return block.release();
      }

    template<typename ParentBlock>
      static Block* subobject(const ParentBlock* parent, const T* object)
      {
        if (!object) return nullptr;
        auto block = std::make_unique<Block>();
        //use aliasing constructor of shared_ptr to keep parent alive
        block->object_ = std::shared_ptr<const T>(parent->object_, object);
        return block.release();
      }
  };

  using Tree_block = Block<Tree>;
}

////////////////////////////////////////////////////////////////////////////////

extern "C" {

  const void* Tree_create(int n)
  {
    return Tree_block::create(n);
  }

  void Tree_dispose(const void* tree)
  {
    delete reinterpret_cast<const Tree_block*>(tree);
  }

  const void* Tree_left(const void* tree)
  {
    auto block = reinterpret_cast<const Tree_block*>(tree);
    return Tree_block::subobject(block, block->object_->left());
  }

  const void* Tree_right(const void* tree)
  {
    auto block = reinterpret_cast<const Tree_block*>(tree);
    return Tree_block::subobject(block, block->object_->right());
  }

  int Tree_data(const void* tree)
  {
    auto block = reinterpret_cast<const Tree_block*>(tree);
    return block->object_->data();
  }
}
