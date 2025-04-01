#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <vector>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <cmath>

// C function that will be called when the python expression ce1.ce_one is evaluated
static PyObject *ce_one_system(PyObject *self, PyObject *args)
{
    std::vector<int> xs, ys;
    PyObject *lines;
    PyArg_ParseTuple(args, "O", &lines);
    
    Py_ssize_t n = PyList_Size(lines);
    for (Py_ssize_t i = 0; i < n; i++) {
        const char *c = PyUnicode_AsUTF8(PyList_GetItem(lines, i));
        int x, y;
        std::istringstream str_stream(c);
        str_stream >> x >> y;
        xs.push_back(x);
        ys.push_back(y);
    }   

    std::sort(xs.begin(), xs.end());
    std::sort(ys.begin(), ys.end());

    int ans = 0;
    for (int i = 0; i < xs.size(); i++) {
        ans += std::abs(xs[i] - ys[i]);
    }

    return PyLong_FromLong(ans);
}


// we need to list its name and address in a “method table”:
static PyMethodDef extensionMethods[] = {
    {"ce_one",  ce_one_system, METH_VARARGS, "Compute sum of differences of smallest to largest pairs"},
    {NULL, NULL, 0, NULL}
};


// The method table must be referenced in the module definition structure:
static struct PyModuleDef extensionmodule = {
    PyModuleDef_HEAD_INIT,
    "extension",   /* name of module */
    "A C implementation of AOC 1.1", /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    extensionMethods
};

// This structure must be passed to the interpreter in the module’s initialization function. 
PyMODINIT_FUNC PyInit_extension(void) { return PyModule_Create(&extensionmodule); }

