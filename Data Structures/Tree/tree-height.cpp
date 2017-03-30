#include <algorithm>
#include <iostream>
#include <vector>
#include <sys/resource.h>
#include <queue>

class Node;

class Node {
public:
    int key;
    Node *parent;
    std::vector<Node *> children;

    Node() {
      this->parent = NULL;
    }

    void setParent(Node *theParent) {
      parent = theParent;
      parent->children.push_back(this);
    }
};

//Build a queue of children out of a group of parent nodes
std::queue<Node> build_children_queue(std::queue<Node> &parents) {

  std::queue< Node > child_nodes;
  while(!parents.empty()) {
    Node root = parents.front();
    std::vector<Node*> root_children = root.children;
    if (!root_children.empty()) 
    {
      for (Node* child : root_children) 
      {
        child_nodes.push(*child);        
      }         
    }
    parents.pop();
  }
  return child_nodes;

}

int main_with_large_stack_space() {
  std::ios_base::sync_with_stdio(0);
  int n;
  std::cin >> n;

  std::vector<Node> nodes;
  nodes.resize(n);
  for (int child_index = 0; child_index < n; child_index++) {
    int parent_index;
    std::cin >> parent_index;
    if (parent_index >= 0)
      nodes[child_index].setParent(&nodes[parent_index]);
    nodes[child_index].key = child_index;
  }

  // Replace this code with a faster implementation
  std::queue<Node> parent_nodes;
  std::queue<Node> child_nodes;

  //Find the root
  for (Node v : nodes) {
    if (v.parent == NULL) {
      parent_nodes.push(v);
      break;
    }
  }

  //Calculate the height by calculating the deepest-reaching node
 int maxHeight = 1;
 while( !( ( child_nodes = build_children_queue(parent_nodes) ).empty()  ) ) {
      parent_nodes.swap(child_nodes);
      maxHeight += 1;    
  }
  
  
  

  std::cout << maxHeight << std::endl;
  
}




int main (int argc, char **argv)
{
  // Allow larger stack space
  const rlim_t kStackSize = 16 * 1024 * 1024;   // min stack size = 16 MB
  struct rlimit rl;
  int result;

  result = getrlimit(RLIMIT_STACK, &rl);
  if (result == 0)
  {
      if (rl.rlim_cur < kStackSize)
      {
          rl.rlim_cur = kStackSize;
          result = setrlimit(RLIMIT_STACK, &rl);
          if (result != 0)
          {
              std::cerr << "setrlimit returned result = " << result << std::endl;
          }
      }
  }

  return main_with_large_stack_space();
}

