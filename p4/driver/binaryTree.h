#ifndef P4_BINARYTREE_H
#define P4_BINARYTREE_H

#include <string>
#include <vector>
#include <variant>

// A nodeValue type variable can either be a string or an integer.
// Go to https://en.cppreference.com/w/cpp/utility/variant for further reading
typedef std::variant<std::string, int> nodeValue;

// A node in a binary tree
class Node {
private:
    int val;
    // A pointer to the left child of this node.
    // It should be null if the left child doe not exist
    Node *left;
    // A pointer to the left child of this node.
    // It should be null if the right child doe not exist
    Node *right;
public:
    // todo: implement this
    Node(const int &val, Node *left = nullptr, Node *right = nullptr);

    ~Node() = default;

    // todo: implement this
    // return the value of the node
    int getVal() const;

    // todo: implement this
    // set the value of the node with {newVal}
    void setVal(const int &newVal);

    // todo: implement this
    // return the pointer to the left child
    Node *getLeft() const;

    // todo: implement this
    // Set the left child of this node
    // If the left child is null, creat a new node with {newVal}
    // If the left child is not null pointer, update the value with {newVal}
    void setLeft(const int &newVal);

    // todo: implement this
    // return the pointer to the right child
    Node *getRight() const;

    // todo: implement this
    // Set the right child of this node
    // If the right child is null, creat a new node with {newVal}
    // If the right child is not null pointer, update the value with {newVal}
    void setRight(const int &newVal);
};

// A binary tree object
class BinaryTree {
private:
    Node *root;         // Root node of the binary tree
public:
    // EFFECTS: Construct an empty binary tree
    BinaryTree() : root(nullptr) {};

    // todo: implement this
    // EFFECTS: Construct a binary tree with a single root node. The value of the root node is {rootValue}
    BinaryTree(const int &rootValue);

    // todo: implement this
    // EFFECTS: Construct a binary tree with a root node.
    BinaryTree(Node *node);

    // todo: implement this
    // Deep copy constructor
    BinaryTree(const BinaryTree &tree);

    // EFFECTS: Construct a binary tree with a list of values, either an integer as value of the node or an empty node flag
    // The empty flag can be any string. The construction will follow the rule of a complete binary tree.
    // Ex. list {0,1,2,3,"","",6,7} will result in a binary tree below
    //           0
    //          / \
    //         /   \
    //        1     2
    //       / \   / \
    //      3         6
    //     /
    //    7
    BinaryTree(std::vector<nodeValue> &source);

    // todo: implement this
    ~BinaryTree();

    // todo: implement this
    // EFFECTS: Return true if the root node is null pointer
    bool empty() const;

    // todo: implement this
    // EFFECTS: find the node with value {key}
    // Assume that the value of all nodes are unique
    Node *find(const int &key) const;

    // todo: implement this
    // EFFECTS: Return the path from the root node to the node with value {key}.
    // The path is encoded by a string only containing '0' and '1'. Each
    // character, from left to right, shows whether to go left (encoded
    // by ‘0’) or go right (encoded by ‘1’) from a node can lead to the
    // target node.
    //
    // For example, we want to find 10 in the following
    // tree
    //
    //                  0
    //                /   \
    //               /      \
    //              1        2
    //             / \      / \
    //                4        6
    //               / \      / \
    //              9   10
    //             / \  / \
    //
    // The returned string should be "011". (Go left from 0, then go right from
    // 1, and finally go right from 4 can lead us to 10.)
    //
    // If {key} is in root node, then return an empty string.
    // If {key} is not in the tree, then return "-1".
    // You can assume that the value of all the nodes are unique in a binary
    // tree.
    std::string findPath(const int &key) const;

    // todo: implement this
    // EFFECTS: Return the terminal node if we can go through the tree starting from the root node and along the {path}.
    // By "can go through the tree", every node along the path should be not null.
    // If we encounter a null node on the halfway, the visit fails.
    //
    // The {path} is encoded by a string only containing '0' and '1'. Each
    // character, from left to right, shows whether to go left (encoded
    // by ‘0’) or go right (encoded by ‘1’) from the current node

    // Return the root node if {path} is empty
    // Return null if we can not go through the tree
    Node *visitThroughPath(const std::string &path) const;

    // todo: implement this
    // EFFECTS: Return the sum of the value of all nodes in the tree.
    // If the tree is empty, return 0.
    int sum() const;

    // todo: implement this
    // EFFECTS: Return the height of the tree,
    // which equals the number of layers of nodes in the tree.
    // Return zero if the tree is empty.
    //
    // For example, the tree
    //
    //                  a
    //                /   \
    //               /      \
    //              b        c
    //             / \      / \
    //                d        e
    //               / \      / \
    //              f   g
    //             / \ / \
    //
    // has height 4.
    // The node a is on the first layer.
    // The nodes b and c are on the second layer.
    // The nodes d and e are on the third layer.
    // The nodes f and g are on the fourth layer.
    int height() const;

    // todo: implement this
    // EFFECTS: Print the value of each node using a pre-order traversal.
    // Separate each value with a space. A pre-order traversal prints the
    // current node first, then recursively visit its left subtree, and then
    // recursively visit its right subtree and so on, until the right-most
    // element is printed.
    //
    // For any node, all the elements of its left subtree
    // are considered as on the left of that node and
    // all the elements of its right subtree are considered as
    // on the right of that node.
    //
    // For example, the tree:
    //
    //                  4
    //                /   \
    //               /     \
    //              2       5
    //             / \
    //            7   3
    //               / \
    //              8   9
    //
    // would print 4 2 7 3 8 9 5
    //
    // An empty tree would print nothing.
    void preOrder() const;

    // todo: implement this
    // EFFECTS: Print the value of each node using a in-order traversal.
    // Separate each {num} with a space. An in-order traversal recursively
    // visit its left subtree, then print the current node,
    // and then recursively visit its right subtree.
    //
    // For any node, all the elements of its left subtree
    // are considered as on the left of that node and
    // all the elements of its right subtree are considered as
    // on the right of that node.
    //
    // For example, the tree:
    //
    //                  4
    //                /   \
    //               /     \
    //              2       5
    //             / \
    //            7   3
    //               / \
    //              8   9
    //
    // would print 7 2 8 3 9 4 5
    //
    // An empty tree would print nothing.
    void inOrder() const;

    // todo: implement this
    // EFFECTS: Print the value of each node using a post-order traversal.
    // Separate each {num} with a space. A post-order traversal recursively
    // visit its left subtree, and then recursively visit its right subtree
    // and then print the current node.
    //
    // For any node, all the elements of its left subtree
    // are considered as on the left of that node and
    // all the elements of its right subtree are considered as
    // on the right of that node.
    //
    // For example, the tree:
    //
    //                  4
    //                /   \
    //               /     \
    //              2       5
    //             / \
    //            7   3
    //               / \
    //              8   9
    //
    // would print 7 8 9 3 2 5 4
    //
    // An empty tree would print nothing.
    void postOrder() const;

    // todo: implement this
    // EFFECTS: Return true if and only if for each root-to-leaf path of the tree,
    // the sum of the value of all nodes along the path is greater than {sum}.
    //
    // Return false if the tree is empty
    //
    // A root-to-leaf path is a sequence of nodes in a tree starting with
    // the root element and proceeding downward to a leaf (an element with
    // no children).
    //
    // For example, the tree:
    //
    //                  4
    //                /   \
    //               /     \
    //              1       5
    //             / \     / \
    //            3   6
    //           / \ / \
    //
    // has three root-to-leaf paths: 4->1->3, 4->1->6 and 4->5.
    // Given the input sum = 9, the path 4->5 has the sum 9, so the function
    // should return false. If the input sum = 7, since all paths have the sums
    // greater than 7, the function should return true.
    bool allPathSumGreater(const int &sum) const;

    // todo: implement this
    // EFFECTS: Return true if this is covered by {tree}
    bool operator<(const BinaryTree &tree) const;

    // todo: implement this
    // EFFECTS: Return true if this is contained by {tree}
    bool operator<<(const BinaryTree &tree) const;

    // todo: implement this
    // EFFECTS: "=" overloading
    BinaryTree &operator=(const BinaryTree &tree);

private:
    // EFFECTS: Create a tree recursively from an array, following the rule of building a complete binary tree.
    // Rule: Suppose the index starts at 0, the left child of the nth element in the array is the (2*(n+1)-1)th element.
    // The right child of the nth element in the array is the (2*(n+1))th element
    // If source[rootIndex] is a string(its value does not matter), it will create an empty node
    Node *createFromVariant(const std::vector<nodeValue> &source, const int &rootIndex);
};


#endif