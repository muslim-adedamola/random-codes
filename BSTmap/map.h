
#ifndef MAP_H_
#define MAP_H_

#include <stdlib.h>

typedef struct _tree_node {
	char *key;
	int   value;
	struct _tree_node *left;
	struct _tree_node *right;
} tree_node;

typedef struct {
	size_t map_size;
	tree_node *root;
} map;


// Creates a new empty map on the heap
map* create_map();

// Destroys the map, and frees up its memory
void destroy_map(map *mp);

// Adds the key-value pair (key, val) to the map
void define(map *mp, char *key, int val);

// Checks if the given key is in the map
_Bool contains_key(map *mp, char *key);

// Returns the value associated with the given key;
// If the key is not there, output an error message to the
// console window, and return INT_MIN
int get_value(map *mp, char *key);

// Returns the number of key-value pairs in the map
size_t map_size(map *mp);

// Removes all of the key-value pairs from the map
void clear_map(map *mp);

// Outputs the key-value pairs in the map to the console window
void print_map(map *mp);


#endif /* MAP_H_ */
