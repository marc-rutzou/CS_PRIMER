#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#define STARTING_CAPACITY 8

//TODO: make typedef
struct DA {
    void * arr[STARTING_CAPACITY]; // array of void pointers
    int length;
    int capacity;
    };

struct DA* DA_new (void) {
    struct DA* pda = (struct DA*) malloc(sizeof(struct DA)); // malloc returns void pointer, cast it to pointer to struct
    (*pda).length = 0;  
    pda->capacity = STARTING_CAPACITY;
    return pda;
}

void DA_free(struct DA *pda) {
    free(pda->arr);
    free(pda);
}

int DA_size(struct DA *da) {
   return (*da).length; 
}

void DA_push (struct DA* pda, void* x) {
    // go to the location that the first void pointer in the array points to

    // length gives where we are in the array

    // (*pda).arr + length == pda->arr[length]   
    // update length
    if (pda->length < pda->capacity)
        pda->arr[pda->length++] = x; //the first void pointer in array is set to the void pointer to x
    else {
        pda->capacity *= 2;
        pda->arr = realloc(pda->arr, pda->capacity * sizeof(void *));
    }
        
}   

void *DA_pop(struct DA *pda) {
    // just decrease length?
    // also return the top value from the stack
    if (pda->length > 0) {
        return pda->arr[--(pda->length)];
    }
    else {
        printf("error: stack empty, can't pop\n");
        return NULL;
    }
}

void DA_set(struct DA *pda, void* x, int i) {
    if (i >= 0 && i < pda->length) 
        pda->arr[i] = x;  // the void pointer at position i is set to point at arg x instead of whatever's in there
    else
        printf("error: i outside dynamic array bounds, can't get\n");
}

void *DA_get(struct DA *pda, int i) {
    if (i >= 0 && i < pda->length) 
        return pda->arr[i];
    else {
        printf("error: i outside dynamic array bounds, can't set\n");
        return NULL;
    }
}

int main() {
    struct DA* pda = DA_new();
    assert(DA_size(pda) == 0);

    int x = 5;
    float y = 12.4;
    DA_push(pda, &x);
    DA_push(pda, &y);

    // cast the pointer to x to right type, b/c you can't dereference a void pointer
    printf("PtrX: %p, x: %d\n", pda->arr[0], * (int *) (pda->arr[0])); 
    printf("PtrY: %p, y: %f\n", pda->arr[1], * (float *) (pda->arr[1])); 

    // pop top of stack
    float val = * (float *) DA_pop(pda);
    printf("popped value: %f\n", val);

    // set/get 
    DA_set(pda, &y, 0);
    printf("PtrX: %p, x: %f\n", pda->arr[0], * (float *) (pda->arr[0])); 
    
    printf("pda: %p, length: %d, arr: %p, pointer to length int: %p", pda, pda->length, pda->arr, &(pda->length));

    // expansion test
    struct DA *da2 = DA_new(); // use another DA to show it doesn't get overriden
    DA_push(da2, &x);
    int i, n = 100 * STARTING_CAPACITY, arr[n];
    for (i = 0; i < n; i++) {
      arr[i] = i;
      DA_push(pda, &arr[i]);
    }
    assert(DA_size(pda) == n);
    for (i = 0; i < n; i++) {
      assert(DA_get(pda, i) == &arr[i]);
    }
    for (; n; n--)
      DA_pop(pda);
    assert(DA_size(pda) == 0);
    assert(DA_pop(da2) == &x); // this will fail if da doesn't expand

    DA_free(pda);
    DA_free(da2);
    printf("OK\n");
}
