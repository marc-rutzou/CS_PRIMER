#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <iostream>
#include <string>
#include <unordered_map>
#include <map>
#include <vector>

// don't use vector class in a loop
// don't use a lot of Python C API
// compile with -O3 flag

/*
TODO:
- most of the time is spend on sscanf
*/

#define MY_MAX_INPUT 100

static PyObject* f(PyObject *self, PyObject *args) {
    PyObject *lines; 
    PyArg_ParseTuple(args, "O", &lines);

    int ans = 0;
    int n_row = (int) PyList_Size(lines);
    bool parse_rules = true;
    std::map<int, int*> rules;

    for (int i = 0; i < n_row; i++) {
        char *row = (char *) PyUnicode_AsUTF8(PyList_GetItem(lines, i));
        if (strcmp(row, "") == 0) {
            parse_rules = false;
            continue; // skip white line
        }

        int x, y;
        if (parse_rules) { 
            sscanf(row, "%d|%d", &x, &y);

            // Allocate new array if key doesn't exist
            if (rules.find(x) == rules.end()) {
                rules[x] = new int[MY_MAX_INPUT]();
            }

            // insert y at the first zero
            for (int j = 0; j < MY_MAX_INPUT; j++) {
                if (rules[x][j] == 0) {
                    rules[x][j] = y;
                    break;
                } 
            }

        } else { 
            
            // updates
            int update[MY_MAX_INPUT];
            int len_update = 0;
            int pos = 0;
            while (sscanf(row, "%d,%n", &update[len_update], &pos) == 1 ) {
                row += pos;
                len_update++;
            }            

            bool valid_update = true;
            bool early_break = false;
            for (int k = 0; k < len_update; k++) {
                if (early_break) break;
                for (int l = k + 1; l < len_update; l++) {
                    bool found = false; 
                    if (rules.find(update[k]) != rules.end()) {
                        int m = 0;
                        while (rules[update[k]][m] != 0) {
                            if (update[l] == rules[update[k]][m]) found = true; 
                            m++;
                        }
                    }
                    if (!found) {
                        valid_update = false;
                        early_break = true;
                    }
                }
            }
            if (valid_update) {
                ans += update[len_update / 2];
            }

        }
    }
    return PyLong_FromLong(ans);
}

static PyObject* f2(PyObject *self, PyObject *args) {
    PyObject *lines; 
    PyArg_ParseTuple(args, "O", &lines);

    int ans = 0;
    int n_row = (int) PyList_Size(lines);
    bool parse_rules = true;
    std::unordered_map<int, int*> rules;

    for (int i = 0; i < n_row; i++) {
        char *row = (char *) PyUnicode_AsUTF8(PyList_GetItem(lines, i));
        if (strcmp(row, "") == 0) {
            parse_rules = false;
            continue; // skip white line
        }

        int x, y;
        if (parse_rules) { 
            sscanf(row, "%d|%d", &x, &y);

            // Allocate new array if key doesn't exist
            if (rules.find(x) == rules.end()) {
                rules[x] = new int[MY_MAX_INPUT]();
            }

            // insert y at the first zero
            for (int j = 0; j < MY_MAX_INPUT; j++) {
                if (rules[x][j] == 0) {
                    rules[x][j] = y;
                    break;
                } 
            }

        } else { 
            
            // updates
            int update[MY_MAX_INPUT];
            int len_update = 0;
            int pos = 0;
            while (sscanf(row, "%d,%n", &update[len_update], &pos) == 1 ) {
                row += pos;
                len_update++;
            }            

            bool valid_update = true;
            bool early_break = false;
            for (int k = 0; k < len_update; k++) {
                if (early_break) break;
                for (int l = k + 1; l < len_update; l++) {
                    bool found = false; 
                    if (rules.find(update[k]) != rules.end()) {
                        int m = 0;
                        while (rules[update[k]][m] != 0) {
                            if (update[l] == rules[update[k]][m]) found = true; 
                            m++;
                        }
                    }
                    if (!found) {
                        valid_update = false;
                        early_break = true;
                    }
                }
            }
            if (valid_update) {
                ans += update[len_update / 2];
            }

        }
    }
    return PyLong_FromLong(ans);
}

static PyObject* f3(PyObject *self, PyObject *args) {
    PyObject *lines; 
    PyArg_ParseTuple(args, "O", &lines);

    int ans = 0;
    int n_row = (int) PyList_Size(lines);
    bool parse_rules = true;
    std::unordered_map<int, int*> rules;

    for (int i = 0; i < n_row; i++) {
        char *row = (char *) PyUnicode_AsUTF8(PyList_GetItem(lines, i));
        if (strcmp(row, "") == 0) {
            parse_rules = false;
            continue; // skip white line
        }

        int x, y;
        if (parse_rules) { 
            sscanf(row, "%d|%d", &x, &y);

            // Allocate new array if key doesn't exist
            if (rules.find(x) == rules.end()) {
                rules[x] = new int[MY_MAX_INPUT]();
            }

            // insert y at the first zero
            for (int j = 0; j < MY_MAX_INPUT; j++) {
                if (rules[x][j] == 0) {
                    rules[x][j] = y;
                    break;
                } 
            }

        } else { 
            
            // updates
            int update[MY_MAX_INPUT];
            int len_update = 0;
            int pos = 0;
            while (sscanf(row, "%d,%n", &update[len_update], &pos) == 1 ) {
                row += pos;
                len_update++;
            }            

            bool valid_update = true;
            for (int k = 0; k < len_update && valid_update; k++) {
                for (int l = k + 1; l < len_update && valid_update; l++) {
                    bool found = false; 
                    if (rules.find(update[k]) != rules.end()) {
                        int m = 0;
                        while (rules[update[k]][m] != 0) {
                            if (update[l] == rules[update[k]][m]) {
                                found = true;
                                break;
                            }
                            m++;
                        }
                    }
                    if (!found) {
                        valid_update = false;
                        break;
                    }
                }
            }
            if (valid_update) {
                ans += update[len_update / 2];
            }

        }
    }
    return PyLong_FromLong(ans);
}



static PyObject* f4(PyObject *self, PyObject *args) {
    PyObject *lines; 
    PyArg_ParseTuple(args, "O", &lines);

    int ans = 0;
    int n_row = (int) PyList_Size(lines);
    bool parse_rules = true;
    std::unordered_map<int, int*> rules;

    for (int i = 0; i < n_row; i++) {
        char *row = (char *) PyUnicode_AsUTF8(PyList_GetItem(lines, i));
        if (strcmp(row, "") == 0) {
            parse_rules = false;
            continue; // skip white line
        }

        int x, y;
        if (parse_rules) { 
            sscanf(row, "%d|%d", &x, &y);

            // Allocate new array if key doesn't exist
            if (rules.find(x) == rules.end()) {
                rules[x] = new int[MY_MAX_INPUT]();
            }

            // insert y at the first zero
            for (int j = 0; j < MY_MAX_INPUT; j++) {
                if (rules[x][j] == 0) {
                    rules[x][j] = y;
                    break;
                } 
            }

        } else { 
            
            // updates
            int update[MY_MAX_INPUT];
            int len_update = 0;
            int pos = 0;
            while (sscanf(row, "%d,%n", &update[len_update], &pos) == 1 ) {
                row += pos;
                len_update++;
            }            

            bool valid_update = true;
            for (int k = 0; k < len_update && valid_update; k++) {
                int *values = rules[update[k]];
                for (int l = k + 1; l < len_update && valid_update; l++) {
                    bool found = false; 
                    if (rules.find(update[k]) != rules.end()) {
                        int m = 0;
                        while (values[m] != 0) {
                            if (update[l] == values[m]) {
                                found = true;
                                break;
                            }
                            m++;
                        }
                    }
                    if (!found) {
                        valid_update = false;
                        break;
                    }
                }
            }
            if (valid_update) {
                ans += update[len_update / 2];
            }

        }
    }
    return PyLong_FromLong(ans);
}

static PyObject* f5(PyObject *self, PyObject *args) {
    PyObject *lines; 
    PyArg_ParseTuple(args, "O", &lines);

    int ans = 0;
    int n_row = (int) PyList_Size(lines);
    bool parse_rules = true;
    
    // Replace map with array of arrays
    int* rules[MY_MAX_INPUT] = {nullptr};  // Initialize all pointers to nullptr

    for (int i = 0; i < n_row; i++) {
        char *row = (char *) PyUnicode_AsUTF8(PyList_GetItem(lines, i));
        if (strcmp(row, "") == 0) {
            parse_rules = false;
            continue;
        }

        int x, y;
        if (parse_rules) { 
            sscanf(row, "%d|%d", &x, &y);

            // Allocate new array if not already allocated
            if (rules[x] == nullptr) {
                rules[x] = new int[MY_MAX_INPUT]();
            }

            // insert y at the first zero
            for (int j = 0; j < MY_MAX_INPUT; j++) {
                if (rules[x][j] == 0) {
                    rules[x][j] = y;
                    break;
                } 
            }

        } else { 
            // updates
            int update[MY_MAX_INPUT];
            int len_update = 0;
            int pos = 0;
            while (sscanf(row, "%d,%n", &update[len_update], &pos) == 1 ) {
                row += pos;
                len_update++;
            }            

            bool valid_update = true;
            for (int k = 0; k < len_update && valid_update; k++) {
                int *values = rules[update[k]];
                for (int l = k + 1; l < len_update && valid_update; l++) {
                    bool found = false; 
                    if (values != nullptr) {  // Replace map lookup
                        int m = 0;
                        while (values[m] != 0) {
                            if (update[l] == values[m]) {
                                found = true;
                                break;
                            }
                            m++;
                        }
                    }
                    if (!found) {
                        valid_update = false;
                        break;
                    }
                }
            }
            if (valid_update) {
                ans += update[len_update / 2];
            }

        }
    }

    // Don't forget to free the allocated arrays
    for (int i = 0; i < MY_MAX_INPUT; i++) {
        delete[] rules[i];
    }

    return PyLong_FromLong(ans);
}

static PyObject* f6(PyObject *self, PyObject *args) {
    PyObject *lines; 
    PyArg_ParseTuple(args, "O", &lines);

    int ans = 0;
    int n_row = (int) PyList_Size(lines);
    bool parse_rules = true;
    
    // Replace map with array of arrays
    int* rules[MY_MAX_INPUT] = {nullptr};  // Initialize all pointers to nullptr

    for (int i = 0; i < n_row; i++) {
        char *row = (char *) PyUnicode_AsUTF8(PyList_GetItem(lines, i));
        if (strcmp(row, "") == 0) {
            parse_rules = false;
            continue;
        }

        if (parse_rules) { 
            // Declare variables before using them
            int x = 0;
            int y = 0;
            
            // Manual parsing
            while (*row >= '0' && *row <= '9') {
                x = x * 10 + (*row - '0');
                row++;
            }
            row++; // skip '|'
            
            while (*row >= '0' && *row <= '9') {
                y = y * 10 + (*row - '0');
                row++;
            }

            // Allocate new array if key doesn't exist
            if (rules[x] == nullptr) {
                rules[x] = new int[MY_MAX_INPUT]();
            }

            // insert y at the first zero
            for (int j = 0; j < MY_MAX_INPUT; j++) {
                if (rules[x][j] == 0) {
                    rules[x][j] = y;
                    break;
                } 
            }

        } else { 
            // Replace sscanf("%d,%n") with manual parsing
            int update[MY_MAX_INPUT];
            int len_update = 0;
            
            while (*row) {
                int num = 0;
                // Parse number
                while (*row >= '0' && *row <= '9') {
                    num = num * 10 + (*row - '0');
                    row++;
                }
                update[len_update++] = num;
                
                // Skip comma if present
                if (*row == ',') row++;
            }

            bool valid_update = true;
            for (int k = 0; k < len_update && valid_update; k++) {
                int *values = rules[update[k]];
                for (int l = k + 1; l < len_update && valid_update; l++) {
                    bool found = false; 
                    if (values != nullptr) {  // Replace map lookup
                        int m = 0;
                        while (values[m] != 0) {
                            if (update[l] == values[m]) {
                                found = true;
                                break;
                            }
                            m++;
                        }
                    }
                    if (!found) {
                        valid_update = false;
                        break;
                    }
                }
            }
            if (valid_update) {
                ans += update[len_update / 2];
            }

        }
    }

    // Don't forget to free the allocated arrays
    for (int i = 0; i < MY_MAX_INPUT; i++) {
        delete[] rules[i];
    }

    return PyLong_FromLong(ans);
}

static PyObject* f7(PyObject *self, PyObject *args) {
    PyObject *lines; 
    PyArg_ParseTuple(args, "O", &lines);

    int ans = 0;
    int n_row = (int) PyList_Size(lines);
    bool parse_rules = true;
    
    // Replace map with array of arrays
    int* rules[MY_MAX_INPUT] = {nullptr};  // Initialize all pointers to nullptr

    for (int i = 0; i < n_row; i++) {
        char *row = (char *) PyUnicode_AsUTF8(PyList_GetItem(lines, i));
        if (strcmp(row, "") == 0) {
            parse_rules = false;
            continue;
        }

        if (parse_rules) { 
            // Declare variables before using them
            int x = 0;
            int y = 0;
            
            // Direct indexing for fixed format "XX|YY"
            x = (row[0] - '0') * 10 + (row[1] - '0');
            y = (row[3] - '0') * 10 + (row[4] - '0');
            
            // Allocate new array if key doesn't exist
            if (rules[x] == nullptr) {
                rules[x] = new int[MY_MAX_INPUT]();
            }

            // insert y at the first zero
            for (int j = 0; j < MY_MAX_INPUT; j++) {
                if (rules[x][j] == 0) {
                    rules[x][j] = y;
                    break;
                } 
            }

        } else { 
            // Replace sscanf("%d,%n") with manual parsing
            int update[MY_MAX_INPUT];
            int len_update = 0;
            
            while (*row) {
                int num = 0;
                // Parse number
                while (*row >= '0' && *row <= '9') {
                    num = num * 10 + (*row - '0');
                    row++;
                }
                update[len_update++] = num;
                
                // Skip comma if present
                if (*row == ',') row++;
            }

            bool valid_update = true;
            for (int k = 0; k < len_update && valid_update; k++) {
                int *values = rules[update[k]];
                for (int l = k + 1; l < len_update && valid_update; l++) {
                    bool found = false; 
                    if (values != nullptr) {  // Replace map lookup
                        int m = 0;
                        while (values[m] != 0) {
                            if (update[l] == values[m]) {
                                found = true;
                                break;
                            }
                            m++;
                        }
                    }
                    if (!found) {
                        valid_update = false;
                        break;
                    }
                }
            }
            if (valid_update) {
                ans += update[len_update / 2];
            }

        }
    }

    // Don't forget to free the allocated arrays
    for (int i = 0; i < MY_MAX_INPUT; i++) {
        delete[] rules[i];
    }

    return PyLong_FromLong(ans);
}

static PyMethodDef Methods[] = {
    {"one_cpp", f, METH_VARARGS, "Function"},
    {"one_cpp2", f2, METH_VARARGS, "Function"},
    {"one_cpp3", f3, METH_VARARGS, "Function"},
    {"one_cpp4", f4, METH_VARARGS, "Function"},
    {"one_cpp5", f5, METH_VARARGS, "Function"},
    {"one_cpp6", f6, METH_VARARGS, "Function"},
    {"one_cpp7", f7, METH_VARARGS, "Function"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Module = {
    PyModuleDef_HEAD_INIT,
    "aoc5cpp",
    NULL,
    -1,
    Methods
};

PyMODINIT_FUNC PyInit_aoc5cpp(void) {
    return PyModule_Create(&Module);
}
