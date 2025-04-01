#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <iostream>

// don't use vector class in a loop
// don't use a lot of Python C API
// compile with -O3 flag

// TODO: 
// - convert recursive to iterative
// - 

#define MAX_NUMS 25

bool is_valid(long long ans, long long numbers[MAX_NUMS], int start, int length) {
    if (length < 2) return (numbers[start] == ans);

    if (numbers[start] > ans) return false;
    
    long long a = numbers[start];
    long long b = numbers[start + 1];
        
    numbers[start + 1] = a * b;
    if (is_valid(ans, numbers, start + 1, length - 1)) return true;

    numbers[start + 1] = a + b;
    if (is_valid(ans, numbers, start + 1, length - 1)) return true;

    numbers[start + 1] = b;
    return false;
}

static PyObject* f(PyObject *self, PyObject *args) {
    char *lines;
    PyArg_ParseTuple(args, "s", &lines);   

    long long total = 0;

    char *p = lines;
    while (*p != '\0') {
        long long ans = 0;
        while (*p != ':') {
            ans = 10 * ans + (long long)(*p - '0');
            p++;
        }
        p += 2; // skip ": "

        // Change to long long array
        long long numbers[MAX_NUMS] = {0};
        int idx = 0;
        while (*p != '\n') {
            long long num = 0;
            while (*p != ' ' and *p != '\n') {
                num = 10 * num + (long long)(*p - '0');
                p++;
            }
            numbers[idx++] = num;
            if (*p == ' ') p++; // skip the space
        }
        p++; // skip newline

        if (is_valid(ans, numbers, 0, idx+1)) {
            total += ans;
        }
    }

    return PyLong_FromLongLong(total);
}

static PyMethodDef Methods[] = {
    {"one_cpp", f, METH_VARARGS, "Function"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Module = {
    PyModuleDef_HEAD_INIT,
    "aoc7cpp",
    NULL,
    -1,
    Methods
};

PyMODINIT_FUNC PyInit_aoc7cpp(void) {
    return PyModule_Create(&Module);
}
