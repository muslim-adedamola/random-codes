#include <stdio.h>
#include <stdlib.h>
#include "stack1.h"


int main()
{
    stack* s1 = create_stack(3);
    for(int i=0; i<=10; i++){
        push(s1, i);
    }
    print_stack(s1);

    pop(s1);
    print_stack(s1);

    clear_stack(s1);
    print_stack(s1);

    return 0;
}
