#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <iostream>
#include <string>
#include <regex>

//NOTE:
// don't use vector class in a loop
// don't use a lot of Python C API
// compile with -O3 flag

// Own code using basic regex library
static PyObject* f2(PyObject *self, PyObject *args) {
    char *input;
    PyArg_ParseTuple(args, "s", &input);
    std::string text = input;

    std::regex pattern("mul\\((\\d{1,3}),(\\d{1,3})\\)");

    int total = 0;
    auto words_begin = std::sregex_iterator(text.begin(), text.end(), pattern); // the first pattern match in the string
    auto words_end = std::sregex_iterator(); // default constructor iterator indicating "no more matches"
    for (std::sregex_iterator i = words_begin; i != words_end; ++i) {
        std::smatch match = *i; // next pattern match
        
        int product = 1;
        for (std::ssub_match group : match) {
            try {
                product *= std::stoi(group.str()); 
            }
            catch (const std::invalid_argument &e) {}
        }
        total += product;
    }
    return PyLong_FromLong(total);
}

static inline int parse_number(const char** p) {
    int num = 0;
    while (**p >= '0' && **p <= '9') {
        num = num * 10 + (**p - '0');
        (*p)++;
    }
    return num;
}

static PyObject* f(PyObject *self, PyObject *args) {
    const char *input;
    PyArg_ParseTuple(args, "s", &input);

    const char *p = input;
    int total = 0;

    bool dont = false;
    while(*p) {

        if (*p == 'd' && strncmp(p, "don't()", 7) == 0) {
            dont = true;
            p += 7;
        } else if (*p == 'd' && strncmp(p, "do()", 4) == 0) {
            dont = false;
            p += 4;
        }

        if (!dont && *p == 'm' && *(p+1) == 'u' && *(p+2) == 'l' && *(p+3) == '(') {
            p += 4;
            
            int x = parse_number(&p);
            
            if (*p != ',') continue;
            p++;

            int y = parse_number(&p);

            if (*p != ')') continue;
            p++;

            total += (x * y);
        } else {
            p++;
        }
    }
    return PyLong_FromLong(total);
}

static PyMethodDef Methods[] = {
    {"one_cpp", f, METH_VARARGS, "Function"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Module = {
    PyModuleDef_HEAD_INIT,
    "aoc3cpp",
    NULL,
    -1,
    Methods
};

PyMODINIT_FUNC PyInit_aoc3cpp(void) {
    return PyModule_Create(&Module);
}
