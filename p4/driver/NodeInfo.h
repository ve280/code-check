#ifndef COMPRESS_H
#define COMPRESS_H
#include "BinaryTree.h"
#include <string>
#include <iostream>

struct NodeInfo {
    int node_index;
    char c; // 0 for left, 1 for right, @ for empty
    NodeInfo():node_index(0), c('@'){}
    NodeInfo(int p, char c):node_index(p), c(c){}
    friend std::ostream& operator<<(std::ostream& os, const NodeInfo& ni);
};

std::ostream& operator<<(std::ostream& os, const NodeInfo& ni) {
    if (ni.c == '0' || ni.c == '1')
        os << "(" << ni.node_index << ", " << ni.c << ")";
    else
        os << "(" << ni.node_index << ", " << '@' << ")";
    return os;
}

std::istream& operator>>(std::istream& is, NodeInfo& ni)
{
    char c, tmp; int n;
    is >> tmp >> n >> tmp >> c >> tmp;
    ni.node_index = n;
    ni.c = c;
    return is;
}

#endif