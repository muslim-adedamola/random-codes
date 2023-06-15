#include <stdio.h>
#include <string.h>
#include "map.h"



int main() {
    map* mp = create_map();
    size_t size = 16;

    for (int i = 0; i< size; i++) {
        char* key;
        asprintf(&key, "key-%d", i);
        define(mp, key, i);
    }

//test define and print
    printf("Define\n");
    print_map(mp);
    printf("\n\n");


//Test map size
    printf("map_size(): %d\n\n\n", (int)map_size(mp));


//  Test boolean contain key
    for (int i = 0; i < ((size % 3) | 3); i++) {
        char* key;
        asprintf(&key, "key-%d", i);
        printf("contains_key(%s): %s\n", key, contains_key(mp, key) ? "TRUE" : "FALSE");
        printf("get_value(%s): %d\n", key, get_value(mp, key));
    }

    char* key = "INVALID KEY";
    printf("contains_key(%s): %s\n", key, contains_key(mp, key) ? "TRUE" : "FALSE");
    printf("get_value(%s): %d\n", key, get_value(mp, key));
    printf("\n");


// Test clear map
    printf("\n\n");
    clear_map(mp);
    printf("\n");

//  Test destroy map
    printf("destroy the map\n");
    size = 20;
     for (int i = 0; i< size; i++) {
        char* key;
        asprintf(&key, "key-%d", i);
        define(mp, key, i);
    }
    print_map(mp);
    destroy_map(mp);

    return 0;
}
