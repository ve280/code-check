#ifndef __DLIST_H__
#define __DLIST_H__

class EmptyList {
    // OVERVIEW: an exception class
};

template <class T>
class Dlist {
    // OVERVIEW: contains a double-ended list of Objects

   public:
    // Operational methods

    bool isEmpty() const;
    // EFFECTS: returns true if list is empy, false otherwise

    void insertFront(T *op);
    // MODIFIES this
    // EFFECTS inserts o at the front of the list

    void insertBack(T *op);
    // MODIFIES this
    // EFFECTS inserts o at the back of the list

    T *removeFront();
    // MODIFIES this
    // EFFECTS removes and returns first object from non-empty list
    //         throws an instance of EmptyList if empty

    T *removeBack();
    // MODIFIES this
    // EFFECTS removes and returns last object from non-empty list
    //         throws an instance of EmptyList if empty

    // This method is provided for part 2. Just skip it.
    friend std::ostream& operator<< (std::ostream& os, const Dlist& dl) {
        for(auto i = dl.first; i != NULL ; i = i->next) {
            os << (*(i->op)) << ' ';
        }
        return os;
    }

    // Maintenance methods
    Dlist();                           // constructor
    Dlist(const Dlist &l);             // copy constructor
    Dlist &operator=(const Dlist &l);  // assignment operator
    ~Dlist();                          // destructor

   private:
    // A private type
    struct node {
        node *next; // (NULL if none)
        node *prev; // (NULL if none)
        T *op;
    };

    node *first;  // The pointer to the first node (NULL if none)
    node *last;   // The pointer to the last node (NULL if none)

    // Utility methods

    void removeAll();
    // EFFECT: called by destructor/operator= to remove and destroy
    //         all list elements

    void copyAll(const Dlist &l);
    // EFFECT: called by copy constructor/operator= to copy elements
    //         from a source instance l to this instance
};

/*
Note: as we have shown in the lecture, for template, we also need
to include the method implementation in the .h file. For this
purpose, we include dlist_impl.h below. Please provide the method
implementation in this file.
*/


#include "DlistImpl.h"

#endif /* __DLIST_H__ */
