#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <iostream>
#include <thread>
#include <chrono>


/*
TODO:
- f2: try to use stack memory by using an oversized grid and filling it partly
- do not fill the grid at all, just use the string
*/

bool find_start(unsigned char *grid, int dim, int *i, int *j) {
    for (int k = 0; k < dim; k++) {
        for (int l = 0; l < dim; l++) {
            if (grid[dim * k + l] == '^') {
                *i = k;
                *j = l;
                return true;
            }
        }
    }
    return false; // if not found
}


bool find_start2(char *grid, int dim, int *i, int *j) {
    for (int k = 0; k < dim; k++) {
        for (int l = 0; l < dim; l++) {
            if (grid[dim * k + l] == '^') {
                *i = k;
                *j = l;
                return true;
            }
        }
    }
    return false; // if not found
}

void print_grid(unsigned char *grid, int dim) {
    // Clear screen using system command
    system("clr");
    
    for (int i = 0; i < dim; i++) {
        for (int j = 0; j < dim; j++) {
            std::cout << grid[dim * i + j];
        }
        std::cout << std::endl;
    }
    
    // Add a small delay to make the animation visible
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

static PyObject* f(PyObject *self, PyObject *args) {

    char *grid_str; // is this on the stack or heap?
    PyArg_ParseTuple(args, "s", &grid_str);

    int dim = 0;
    char *p = grid_str;
    while (*p++ != '\n') { dim++; }

    unsigned char *grid = (unsigned char *) malloc(dim * dim * sizeof(unsigned char));
    
    // loop over string to fill grid
    char *p2 = grid_str;
    for (int i = 0; i < dim; i++) {
        for (int j = 0; j < dim; j++) {
            grid[dim * i + j] = (unsigned char) *p2++;
            if (j == dim - 1) { p2++; } // skip newline
        }
    }

    int i, j;
    find_start(grid, dim, &i, &j);
    // printf("Starting position: %d, %d\n", i, j);

    int delta[4][2] = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
    int delta_idx = 0;

    int count = 0;
    int nxt_i, nxt_j;
    while (i != 0 && i != dim - 1 && j != 0 && j != dim - 1) {
        if (grid[i * dim + j] != 'X') {
            count++;
            grid[i * dim + j] = 'X';
        } 

        nxt_i = i + delta[delta_idx][0];
        nxt_j = j + delta[delta_idx][1];

        if (grid[nxt_i * dim + nxt_j] == '#') {
            delta_idx = delta_idx < 3 ? delta_idx + 1 : 0; // 3 = len(delta) - 1
            i = i + delta[delta_idx][0];
            j = j + delta[delta_idx][1];
        } else {
            i = nxt_i;
            j = nxt_j;
        }
        // print_grid(grid, dim);
    }

    free(grid);
    return PyLong_FromLong(count + 1);
}

// now with oversized stack memory
static PyObject* f2(PyObject *self, PyObject *args) {

    char *grid_str;
    PyArg_ParseTuple(args, "s", &grid_str);

    int dim = 0;
    char *p = grid_str;
    while (*p++ != '\n') { dim++; }

    // unsigned char *grid = (unsigned char *) malloc(dim * dim * sizeof(unsigned char));
    unsigned char grid[200 * 200];
    
    // loop over string to fill grid
    char *p2 = grid_str;
    for (int i = 0; i < dim; i++) {
        for (int j = 0; j < dim; j++) {
            grid[dim * i + j] = (unsigned char) *p2++;
            if (j == dim - 1) { p2++; } // skip newline
        }
    }

    int i, j;
    find_start(grid, dim, &i, &j);
    // printf("Starting position: %d, %d\n", i, j);

    int delta[4][2] = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
    int delta_idx = 0;

    int count = 0;
    int nxt_i, nxt_j;
    while (i != 0 && i != dim - 1 && j != 0 && j != dim - 1) {
        if (grid[i * dim + j] != 'X') {
            count++;
            grid[i * dim + j] = 'X';
        } 

        nxt_i = i + delta[delta_idx][0];
        nxt_j = j + delta[delta_idx][1];

        if (grid[nxt_i * dim + nxt_j] == '#') {
            delta_idx = delta_idx < 3 ? delta_idx + 1 : 0; // 3 = len(delta) - 1
            i = i + delta[delta_idx][0];
            j = j + delta[delta_idx][1];
        } else {
            i = nxt_i;
            j = nxt_j;
        }
        // print_grid(grid, dim);
    }

    // free(grid);
    return PyLong_FromLong(count + 1);
}

// now with using the string directly
static PyObject* f3(PyObject *self, PyObject *args) {
    char *grid_str;
    PyArg_ParseTuple(args, "s", &grid_str);

    int dim = 0;
    char *p = grid_str;
    while (*p++ != '\n') { dim++; }
    
    int i, j;
    find_start2(grid_str, dim + 1, &i, &j); // dim + 1 to account for newlines
    
    int delta[4][2] = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
    int delta_idx = 0;

    int count = 0;
    int nxt_i, nxt_j;
    while (i != 0 && i != dim - 1 && j != 0 && j != dim - 1) {
        if (grid_str[(dim + 1) * i + j] != 'X') { // dim + 1 to account for newlines
            count++;
            grid_str[(dim + 1) * i + j] = 'X';
        } 

        nxt_i = i + delta[delta_idx][0];
        nxt_j = j + delta[delta_idx][1];

        if (grid_str[(dim + 1) * nxt_i + nxt_j] == '#') { // dim + 1 to account for newlines
            delta_idx = delta_idx < 3 ? delta_idx + 1 : 0;
            i = i + delta[delta_idx][0];
            j = j + delta[delta_idx][1];
        } else {
            i = nxt_i;
            j = nxt_j;
        }
    }

    return PyLong_FromLong(count + 1);
}

// now with a simpler while condition, because of annotation
static PyObject* f4(PyObject *self, PyObject *args) {
    char *grid_str;
    PyArg_ParseTuple(args, "s", &grid_str);

    int dim = 0;
    char *p = grid_str;
    while (*p++ != '\n') { dim++; }
    dim++;
    
    int i, j;
    find_start2(grid_str, dim, &i, &j); // dim + 1 to account for newlines
    
    int delta[4][2] = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
    int delta_idx = 0;

    int count = 0;
    int nxt_i, nxt_j;
    while (i > 0 && i < dim - 2 && j > 0 && j < dim - 2) {
        if (grid_str[dim * i + j] != 'X') {
            count++;
            grid_str[dim * i + j] = 'X';
        } 

        nxt_i = i + delta[delta_idx][0];
        nxt_j = j + delta[delta_idx][1];

        if (grid_str[dim * nxt_i + nxt_j] == '#') { // dim + 1 to account for newlines
            delta_idx = delta_idx < 3 ? delta_idx + 1 : 0;
            i = i + delta[delta_idx][0];
            j = j + delta[delta_idx][1];
        } else {
            i = nxt_i;
            j = nxt_j;
        }
    }

    return PyLong_FromLong(count + 1);
}

static PyMethodDef Methods[] = {
    {"one_cpp", f, METH_VARARGS, "Function"},
    {"one_cpp2", f2, METH_VARARGS, "Function"},
    {"one_cpp3", f3, METH_VARARGS, "Function"},
    {"one_cpp4", f4, METH_VARARGS, "Function"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Module = {
    PyModuleDef_HEAD_INIT,
    "aoc6cpp",
    NULL,
    -1,
    Methods
};

PyMODINIT_FUNC PyInit_aoc6cpp(void) {
    return PyModule_Create(&Module);
}
