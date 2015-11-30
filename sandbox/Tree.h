struct Node
{
  int data_;
  std::shared_ptr<Node> left_;
  std::shared_ptr<Node> right_;
};

class Tree
{
  std::shared_ptr<Node> head_;

  Tree* left_subtree()
  {
    auto left_tree = std::make_unique<Tree>();
    if (!head_) return left_tree.release();
    left_tree->head_ = head_->left_;
    return left_tree.release();
  }

  Tree* right_subtree()
  {
    auto right_tree = std::make_unique<Tree>();
    if (!head_) return right_tree.release();
    right_tree->head_ = head_->right_;
    return right_tree.release();
  }

  int* data()
  {
    if (!head_) return nullptr;
    return &head_->data_;
  }
};
