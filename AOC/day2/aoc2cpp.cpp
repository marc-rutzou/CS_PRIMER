#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <iostream>
#include <cstdlib>
#include <vector>
#include <sstream>


static PyObject* f(PyObject *self, PyObject *args) {
    PyObject *lines;
    PyArg_ParseTuple(args, "O", &lines); // "O": format as generic py object
    
    Py_ssize_t num_lines = PyList_Size(lines);
    int num_safe = 0;
    for (Py_ssize_t i = 0; i < num_lines; i++) {
        const char *report = PyUnicode_AsUTF8(PyList_GetItem(lines, i));

        std::istringstream str_stream(report);
        int number;
        std::vector<int> levels;
        while (str_stream >> number) {
            levels.push_back(number);
        }

        int sign_sum = 0;
        int delta;
        bool found_mistake = false;
        for (size_t i = 0; i < levels.size() - 1; i++) {
            delta = levels[i+1] - levels[i];

            if (std::abs(delta) == 0 || std::abs(delta) > 3) {
                found_mistake = true;
            }

            if (delta > 0) {
                sign_sum++;
            } else {
                sign_sum--;
            }
        }
        
        if (!found_mistake && std::abs(sign_sum) == (levels.size() - 1)) {
            num_safe++;
        }
    }
    return PyLong_FromLong(num_safe);
}

static PyObject* f2(PyObject *self, PyObject *args) {
    PyObject *lines;
    PyArg_ParseTuple(args, "O", &lines); // "O": format as generic py object
    
    int num_safe = 0;
    Py_ssize_t num_lines = PyList_Size(lines);
    for (int i = 0; i < num_lines; i++) {
        const char *report = PyUnicode_AsUTF8(PyList_GetItem(lines, i));

        int n = 0;
        int levels[10] = {0}; // init to zero
        const char *ptr = report; // pointer to iterate through string
        while (*ptr != '\n' && n < 10 && *ptr != '\0') {
            int num = 0;
            while (*ptr >= '0' && *ptr <= '9') {
                num = num * 10 + (*ptr - '0');
                ptr++;
            } 
            levels[n++] = num;

            while (*ptr == ' ') ptr++;
        }

        int sign_sum = 0;
        int delta;
        bool found_mistake = false;
        for (int i = 0; i < n - 1; i++) {
            delta = levels[i+1] - levels[i];

            if (std::abs(delta) == 0 || std::abs(delta) > 3) {
                found_mistake = true;
            }

            if (delta > 0) {
                sign_sum++;
            } else {
                sign_sum--;
            }
        }
        
        if (!found_mistake && std::abs(sign_sum) == (n - 1)) {
            num_safe++;
        } 
    }
    return PyLong_FromLong(num_safe);
}

static PyMethodDef Methods[] = {
    {"one_cpp", f, METH_VARARGS, "Function"},
    {"one_cpp2", f2, METH_VARARGS, "Function2"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Module = {
    PyModuleDef_HEAD_INIT,
    "aoc2cpp",   // name
    NULL,        // documentation
    -1,
    Methods
};

PyMODINIT_FUNC PyInit_aoc2cpp(void) { // PyInit_<name>
    return PyModule_Create(&Module);
}
