#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject* f(PyObject *self, PyObject *args) {

}

static PyMethodDef Methods[] = {
    {/*TODO name function*/, f, METH_VARARGS, "Function" /*description*/},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Module = {
    PyModuleDef_HEAD_INIT,
    /*TODO name extension*/,
    NULL, // documentation
    -1,
    Methods
};

PyMODINIT_FUNC PyInit_/*TODO name extension*/(void) {
    return PyModule_Create(&Module);
}
