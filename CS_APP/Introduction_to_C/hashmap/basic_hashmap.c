#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include <assert.h>

#define STARTING_BUCKETS 8
#define MAX_KEY_SIZE 100

// TODO: don't make the array fixed size, make it struct node**, so you can change the size
// TODO: free hashmap and all nodes 

struct node {
    char* key;
    void* value;
    struct node* next;
};

// an array of pointers to the first node
struct Hashmap {
    struct node* buckets[STARTING_BUCKETS];
};

// key -> bucket_number (int); needs to be deterministic
int hash(char *key) {
    /* hash input string to int by taking sum of first 3 letters ASCII value */
    int hashed_value = 0;
    for (int i = 0; i<3 && key[i] != '\0'; i++) {
        hashed_value += key[i] - 'a';
    }
    return hashed_value % STARTING_BUCKETS;
}

struct node* Node_new() {
    struct node* pn = (struct node*) malloc(sizeof(struct node));
    pn->next = NULL;
    return pn;
}

struct Hashmap* Hashmap_new() {
    struct Hashmap* phm = (struct Hashmap*) malloc(sizeof(struct Hashmap));

    // set each pointer to a first node
    for (int i = 0; i < STARTING_BUCKETS; i++) {
        (phm->buckets[i]) = Node_new();
    }
    return phm;
}

int Hashmap_set(struct Hashmap* phm, char* key, void* value) { // pointer to value otherwise passed by value
    // hash key to bucket number
    int bucket_number = hash(key); 

    // pointer to first node
    struct node* Ptr_node = phm->buckets[bucket_number];

    // if you arrive at a node that points to nothing, you are at the end of the linked list
    char key_in_list = 0;
    while (Ptr_node->next != NULL) {
        if (strcmp(Ptr_node->key, key) == 0) {
            key_in_list = 1; 
            break;
        }
        else {
            Ptr_node = Ptr_node->next;
        }
    }

    Ptr_node->value = value;
    if (!key_in_list) {
        // arrived at the final node
        Ptr_node->key = strdup(key);
        struct node* Ptr_new_node = Node_new();
        Ptr_node->next = Ptr_new_node;
    }
    return 0;
}

void* Hashmap_get(struct Hashmap* phm, char* key) {
    int bucket_number = hash(key);
    struct node* Ptr_node = phm->buckets[bucket_number];

    char key_in_list = 0;
    while (Ptr_node->next != NULL) {
        if (!strcmp(Ptr_node->key, key))
            return Ptr_node->value;
        Ptr_node = Ptr_node->next;
    }
    return NULL;
}


int main() {
    struct Hashmap* h = Hashmap_new();
    // next node in array = char pointer 8 + int 4 + 4 alignment bits + node pointer 8
    printf("\nstart hashmap: %p, start of bucket array: %p, next node: %p\n", h, h->buckets, (h->buckets)+1); 

    // basic get/set functionality
    int a = 5;
    float b = 7.2;
    Hashmap_set(h, "item a", &a);
    Hashmap_set(h, "item b", &b);
    assert(Hashmap_get(h, "item a") == &a);
    assert(Hashmap_get(h, "item b") == &b);

    // using the same key should override the previous value
    int c = 20;
    Hashmap_set(h, "item a", &c);
    assert(Hashmap_get(h, "item a") == &c);

    // handle collisions correctly
    // note: this doesn't necessarily test expansion
    int i, n = STARTING_BUCKETS * 10, ns[n];
    char key[MAX_KEY_SIZE];
    for (i = 0; i < n; i++) {
    ns[i] = i;
    sprintf(key, "item %d", i);
    Hashmap_set(h, key, &ns[i]);
    }
    for (i = 0; i < n; i++) {
    sprintf(key, "item %d", i);
    assert(Hashmap_get(h, key) == &ns[i]);
    }

}
