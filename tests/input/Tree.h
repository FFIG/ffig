#include "ffig/attributes.h"
#include <memory>
#include <random>

static std::mt19937 mt;
static std::uniform_int_distribution<int> d(1,10);
static auto gen = []{return d(mt);};

class FFIG_EXPORT Tree
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

  const Tree* left_subtree() const
  {
    return left_.get();
  }

  const Tree* right_subtree() const
  {
    return right_.get();
  }

  int data() const
  {
    return data_;
  }
  
  void set_data(int x)
  {
    data_ = x;
  }

};

