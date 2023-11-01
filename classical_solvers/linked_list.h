#include <stdexcept>

template<typename T>
class Node {
public:
    Node(T value) {
        this->value = value;
        next = nullptr;
        previous = nullptr;
    }
    T value;
    Node<T>* next;
    Node<T>* previous;
};

template <typename T>
class LinkedList {
public:
    LinkedList<T>() {
        size = 0;
        start = nullptr;
        end = nullptr;
    }
    
    void put(T value) {
        Node<T> *n = new Node<T>(value);
        if (size == 0) {
            start = n;
            end = start;
        } else {
            n->previous = end;
            end->next = n;
            end = n;
        }
        size++;
    }
    
    T pop() {
        T value;
        if (size == 0) {
            std::runtime_error("The linked list is empty, there is nothing to pop.");
        }

        if (size == 1) {
            value = start->value;
            delete start;
            start = nullptr;
            end = nullptr;
        } else {
            Node<T> *n = end->previous;
            value = end->value;
            delete end;
            end = n;
            end->next = nullptr;
        }
        size--;

        return value;
    }

    Node<T>* getStartNode() {
        return start;
    }

    int getSize() {
        return size;
    }

private:
    Node<T>* start;
    Node<T>* end;
    int size;
};