#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "map.h"

// Creates a new empty map on the heap
map* create_map(){
    map* mp = malloc(sizeof(mp));
    mp->root = NULL;
    mp->map_size=0;

    return mp;
}

// Destroys the map, and frees up its memory
void destroy_map(map *mp){
    clear_map(mp);
    free(mp);
    printf("Destroyed map: %p\n\n", (void*)mp);
}

tree_node* insert(tree_node *root, tree_node* x, map *mp)
{
    //searching for the place to insert
    if(root==NULL) {
        return x;
        }
    if(strcmp(root->key, x->key) < 0){ // x is greater. Should be inserted to right
        root->right = insert(root->right, x, mp);
        mp->map_size += 1;
        }
    else if(strcmp(root->key, x->key) > 0) { // x is smaller should be inserted to left
        root->left = insert(root->left, x, mp);
        mp->map_size += 1;
        }
    else {
        root->value = x-> value;
    }
    return root;
}

// Adds the key-value pair (key, val) to the map
void define(map *mp, char *key, int val){
    tree_node* trn = malloc(sizeof(tree_node));
    trn->key = key;
    trn->value = val;
    trn->left = NULL;
    trn->right = NULL;

    if(mp->root==NULL){
        mp->root = trn;
        return;
    }
    insert(mp->root, trn, mp);

}


// Checks if the given key is in the map
_Bool contains_key(map *mp, char *key){
    tree_node* trn = mp->root;

    while(trn) {

        if(strcmp(trn->key, key) < 0){
            trn = trn->left;
        }
        else if(strcmp(trn->key, key) > 0){
            trn = trn->right;
        }
        else{
            return 1;
        }
    }

    return 0;
}


// Returns the value associated with the given key;
// If the key is not there, output an error message to the
// console window, and return INT_MIN
int get_value(map *mp, char *key){
    tree_node* trn = mp->root;

    while(trn) {
        if(strcmp(trn->key, key) < 0){
            trn = trn->left;
        }
        else if (strcmp(trn->key, key) > 0){
            trn = trn->right;
        }
        else {
            return trn->value;
        }
    }
    printf("ERROR: there is no such element\n");
    return INT_MIN;

}


// Returns the number of key-value pairs in the map
size_t map_size(map *mp){
    return mp->map_size;
}

//self-defined
void preOrderClear(map *mp, tree_node* trn){
    if(trn == NULL){
        return;
    }

    preOrderClear(mp, trn->left);
    preOrderClear(mp, trn->right);
    free(trn);
    mp->map_size--;
}

// Removes all of the key-value pairs from the map
void clear_map(map *mp){
    preOrderClear(mp, mp->root);
    mp->root = NULL;
    printf("clear the map\n");
    print_map(mp);
    printf("map_size is %d\n", (int)map_size(mp));
}

void inorder(tree_node* trn)
{
    if(trn==NULL){
        return;
    }
    if(trn!=NULL) // checking if the root is not null
    {
        inorder(trn->left); // visiting left child
        printf("%s %d, ", trn->key, trn->value); // printing data at root
        inorder(trn->right);// visiting right child
    }
}


// Outputs the key-value pairs in the map to the console window
void print_map(map *mp){
    inorder(mp->root);
}
