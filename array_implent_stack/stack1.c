#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include "stack1.h"

// Creates a new empty stack on the heap
stack* create_stack(size_t array_size)
{
    stack *stk = (stack*)malloc(sizeof(stack));

    stk->array_size = array_size;       //size of cup
    stk->stack_size = 0;                //volume of water in cup

    stk->values = malloc(array_size*sizeof(int));  //values is the cup

    return stk;

}

// Adds the value val to the top of the stack
void push(stack *stk, int val)
{
    if(stk->stack_size == stk->array_size - 1)
    {
        int* values = (int*)malloc(2*stk->array_size*sizeof(int));      //taking a bigger cup
        stk->array_size = 2*stk->array_size;
        for(int i=0; i<stk->stack_size; i++)    //copying over the water in the cup to a bigger cup
            values[i] = stk->values[i];
        free(stk->values);
        stk->values = values;
    }
    stk->values[stk->stack_size] = val; // put new water in the cup
    stk->stack_size = stk->stack_size + 1;  //update water volume
}


// Destroys the stack, and frees up its memory
void destroy_stack(stack *stk)
{
    free(stk->values);      //pour all the water to nowhere
    free(stk);              //dispose cup
}


// Removes and returns the topmost item of the stack
int pop(stack *stk){
    if(stk->stack_size == 0){
        printf("There is no element in the stack\n");
        return INT_MIN;
    }
    int value = stk->values[stk->stack_size - 1];       //drinking water from the cup
    stk->stack_size = stk->stack_size - 1;
    return value;

}

// Returns the topmost item of the stack, without changing the stack
int peek_top(stack *stk){
    if(stk->stack_size == 0){
        printf("There is no element in the stack\n");       //checks the value in the cup
        return INT_MIN;
    }
    int value = stk->values[stk->stack_size - 1];
    return value;

}

// Returns the number of items on the stack
size_t stack_size(stack *stk){      //gives the volume of water in cup
    return stk->stack_size;
}

// Removes all of the items from the stack
void clear_stack(stack *stk){           //pouring all the water from cup to nowhere.
    free(stk->values);
    stk->values = (int*)malloc(stk->array_size*sizeof(int));
    stk->stack_size = 0;
}

// Outputs the items in the stack to the console window
void print_stack(stack *stk)
{
    int i;                  //shows every piece of water
    printf("Stack: ");
    for(i=0; i<stk->stack_size; i++)
        printf("%d ", stk->values[i] );
    printf("\n");

}


