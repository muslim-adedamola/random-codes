
#ifndef STACK_H_
#define STACK_H_

#include <stdlib.h>

typedef struct _node {
	int value;
	struct _node *link;
} node;

typedef struct {
	size_t stack_size;
	node *top;
} stack;


// Creates a new empty stack on the heap
stack* create_stack();

// Destroys the stack, and frees up its memory
void destroy_stack(stack *stk);

// Adds the value val to the top of the stack
void push(stack *stk, int val);

// Removes and returns the topmost item of the stack
int pop(stack *stk);

// Returns the topmost item of the stack, without changing the stack
int peek_top(stack *stk);

// Returns the number of items on the stack
size_t stack_size(stack *stk);

// Removes all of the items from the stack
void clear_stack(stack *stk);

// Outputs the items in the stack to the console window
void print_stack(stack *stk);

#endif /* STACK_H_ */
