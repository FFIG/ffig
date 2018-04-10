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
  
  // FIXME: Should not be noexcept as it allocates
  Tree(int levels=0) noexcept 
  {
    data_ = gen();
    if ( levels <= 0 ) return;
    left_ = std::make_shared<Tree>(levels-1);
    right_ = std::make_shared<Tree>(levels-1);
  }

  Tree* left_subtree() const noexcept
  {
    return left_.get();
  }

  Tree* right_subtree() const noexcept
  {
    return right_.get();
  }

  int data() const noexcept
  {
    return data_;
  }
  
  void set_data(int x) noexcept
  {
    data_ = x;
  }

};

