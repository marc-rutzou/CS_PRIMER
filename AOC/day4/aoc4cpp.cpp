#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <iostream>
#include <cstring>

// don't use vector class in a loop
// don't use a lot of Python C API
// compile with -O3 flag

// TODO: dont first put everything in a grid

static PyObject* f(PyObject *self, PyObject *args) {
    int cases[8][4][2] = {
        {{0, 0}, {0, 1}, {0, 2}, {0, 3}},
        {{0, 3}, {0, 2}, {0, 1}, {0, 0}},
        {{0, 0}, {1, 0}, {2, 0}, {3, 0}},
        {{3, 0}, {2, 0}, {1, 0}, {0, 0}},
        {{0, 0}, {1, 1}, {2, 2}, {3, 3}},
        {{3, 3}, {2, 2}, {1, 1}, {0, 0}},
        {{0, 3}, {1, 2}, {2, 1}, {3, 0}},
        {{3, 0}, {2, 1}, {1, 2}, {0, 3}},
    };
    char *KEY = "XMAS";

    PyObject *lines;
    PyArg_ParseTuple(args, "O", &lines);

    int n_row = (int) PyList_Size(lines); // potential overflow problems if size > INT_MAX
    int n_col = strlen( (char *) PyUnicode_AsUTF8(PyList_GetItem(lines, 0))); // assume input is square
    char grid[n_row][n_col];

    // fill grid
    for (int i = 0; i < n_row; i++) {
        char *row = (char *) PyUnicode_AsUTF8(PyList_GetItem(lines, i));
        for (int j = 0; j < n_col; j++) {
            grid[i][j] = *(row + j);
        }
    }
    
    int count = 0;
    for (int i = 0; i < n_row; i++) {
        for (int j = 0; j < n_col; j++) {

            for (int x = 0; x < 8; x++) {
                bool found = false;
                for (int y = 0; y < 4; y++) {
                    int di = cases[x][y][0];
                    int dj = cases[x][y][1];
                    if (i + di < n_row && j + dj < n_col) {
                        if (KEY[y] == grid[i + di][j + dj]) {
                            found = true; 
                        } else { 
                            found = false; 
                            break; // go to the next case
                        }
                    } else { 
                        found = false;
                        break; 
                        }
                }
                if (found) {
                    count++;
                    //break;
                } 
                found = false;
            }
        }
    }
    return PyLong_FromLong(count);
}

static PyMethodDef Methods[] = {
    {"one_cpp", f, METH_VARARGS, "Function"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Module = {
    PyModuleDef_HEAD_INIT,
    "aoc4cpp",
    NULL,
    -1,
    Methods
};

PyMODINIT_FUNC PyInit_aoc4cpp(void) {
    return PyModule_Create(&Module);
}
