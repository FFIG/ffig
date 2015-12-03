#include <memory>
#include <random>

static std::mt19937 mt;
static std::uniform_int_distribution<int> d(1,10);
static auto gen = []{return d(mt);};

static int global_tree_count = 0;

class Tree
{
  int data_;
  std::shared_ptr<Tree> left_;
  std::shared_ptr<Tree> right_;

  public:

  Tree(int levels=0)
  {
    ++global_tree_count;
    data_ = gen();
    if ( levels <= 0 ) return;
    left_ = std::make_shared<Tree>(levels-1);
    right_ = std::make_shared<Tree>(levels-1);
  }

  ~Tree()
  {
    --global_tree_count;
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

namespace api_obj {

  template<typename T, typename ...Ts>
    static std::shared_ptr<T>* create(Ts&&...ts)
    {
      return new std::shared_ptr<T>(std::make_shared<T>(std::forward<Ts>(ts)...));
    }

  template<typename Parent, typename Subobject>
    static std::shared_ptr<const Subobject>* subobject(const std::shared_ptr<const Parent>* parent, const Subobject* object)
    {
      if (!object) return nullptr;
      //use aliasing constructor of shared_ptr to keep parent alive
      return new std::shared_ptr<const Subobject>(*parent, object);
    }
} // end namespace api_obj

using Tree_ptr = const std::shared_ptr<const Tree>*;

////////////////////////////////////////////////////////////////////////////////

extern "C" {

  const void* Tree_create(int n)
  {
    return api_obj::create<Tree>(n);
  }

  void Tree_dispose(const void* tree)
  {
    delete reinterpret_cast<const Tree_ptr>(tree);
  }

  const void* Tree_left(const void* tree)
  {
    auto ptr = reinterpret_cast<const Tree_ptr>(tree);
    return api_obj::subobject(ptr, (*ptr)->left());
  }

  const void* Tree_right(const void* tree)
  {
    auto ptr = reinterpret_cast<const Tree_ptr>(tree);
    return api_obj::subobject(ptr, (*ptr)->right());
  }

  int Tree_data(const void* tree)
  {
    auto ptr = reinterpret_cast<const Tree_ptr>(tree);
    return (*ptr)->data();
  }

  int Tree_count()
  {
    return global_tree_count;
  }
}
