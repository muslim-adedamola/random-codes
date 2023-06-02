#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include "stack2.h"


// Creates a new empty stack on the heap
stack* create_stack(){

    stack *stk = (stack*)malloc(sizeof(stack));
    stk->top = NULL;

    stk->stack_size =0;

    return stk;
}

// Destroys the stack, and frees up its memory
void destroy_stack(stack *stk){
    free(stk->top->value);
    free(stk);
}

// Adds the value val to the top of the stack
void push(stack *stk, int val){
    node* new_node = (node*)malloc(sizeof(node));
    new_node->value = val;
    new_node->link = stk->top;
    stk->top = new_node;
    stk->stack_size += 1;
}

// Removes and returns the topmost item of the stack
int pop(stack *stk){
    node* new_node;
    if(stk->top == NULL) {
        printf("There is no element in the stack\n");
        return INT_MIN;
    }
    new_node = stk->top;
    stk->top = stk->top->link;
    free(new_node);
    stk->stack_size -= 1;

}

// Returns the topmost item of the stack, without changing the stack
int peek_top(stack *stk){
    if(stk->top == NULL) {
        printf("There is no element in the stack\n");
        return INT_MIN;
    }
    return stk->top->value;
}

// Returns the number of items on the stack
size_t stack_size(stack *stk){
    return stk->stack_size;
}

// Removes all of the items from the stack
void clear_stack(stack *stk){
    free(stk->top->value);
    stk->stack_size = 0;

}

// Outputs the items in the stack to the console window
void print_stack(stack *stk){

    node* new_node;
    new_node = stk->top;

    if(stk->top == NULL) {
        printf("There is no element in the stack\n");
        return INT_MIN;
    }

    else{
    printf("The Stack Elements are: ");

    while(new_node){
        printf("%d ", new_node->value);
        new_node = new_node->link;
    }
    printf("\n"); }
}







