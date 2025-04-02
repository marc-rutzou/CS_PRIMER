#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *cvarint_encode(PyObject *self, PyObject *args) {
    uint64_t n;
    if (!PyArg_ParseTuple(args, "K", &n))
        return NULL;
    printf("\n Input value (uint64): %llu\n", n);

    uint8_t part, out[8]; // max 8 uint8_t's to get uint64_t 
    int i = 0;
    while (n > 0) {
        part = n & 0x7f;
        n >>= 7;
        printf("\n Next number (decimal): %llu\n", n);
        if (n > 0) {
            part |= 0x80;
        }
        else {       
            out[i] = part;
            printf("\n out[%d]  (decimal): %d; (hex): %x\n", i, out[i], out[i]);
            i++;
            break;
        }
        out[i] = part;
        i++;
        printf("\n out[%d]  (decimal): %d; (hex): %x\n", i, out[i], out[i]);
    }
    
    printf("i: %d", i);
    return PyBytes_FromStringAndSize((char *)out, i);
}

static PyObject *cvarint_decode(PyObject *self, PyObject *args) {
}

static PyMethodDef CVarintMethods[] = {
    {"encode", cvarint_encode, METH_VARARGS, "Encode an integer as varint."},
    {"decode", cvarint_decode, METH_VARARGS,
     "Decode varint bytes to an integer."},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef cvarintmodule = {
    PyModuleDef_HEAD_INIT, "cvarint",
    "A C implementation of protobuf varint encoding", -1, CVarintMethods};

PyMODINIT_FUNC PyInit_cvarint(void) { return PyModule_Create(&cvarintmodule); }
