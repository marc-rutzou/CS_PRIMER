/*
PLAN
- [ ] bitarray
- [ ] less Python C API, 
- [ ] compiler arguments
- [ ] not a lot of conversion
- [ ] improve branch prediction
- [ ] one long array over nested array for better caching performance (not split in memory)
*/

// TODO: say almost now Python C API


#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <iostream>
#include <map>
#include <vector>
#include <set>
#include <unordered_map>
#include <unordered_set>


static PyObject* f2(PyObject *self, PyObject *args) {
    PyObject* page;
    PyArg_ParseTuple(args, "O", &page);
    
    // convert page into Py list
    PyObject* lines = PyUnicode_Splitlines(page, 0);
    Py_ssize_t n_lines = PyList_Size(lines);

    std::map<int, std::set<int> > rules;

    int total = 0;
    bool parsing_rules = true;
    for (Py_ssize_t n = 0; n < n_lines; n++) {
        PyObject *line_obj = PyList_GetItem(lines, n);
        char *line = (char *) PyUnicode_AsUTF8(line_obj);

        if (strcmp(line, "") == 0) {
            parsing_rules = false;
            continue;
        }

        if (parsing_rules) {
            int x = 0, y = 0;
            sscanf(line, "%d|%d", &x, &y);  
            rules[x].insert(y);
        } else {
            std::vector<int> update;
            int pos = 0; // number of chars processed by sscanf
            int num = 0; // next number extracted by sscanf
            while(sscanf(line, "%d%n", &num, &pos) == 1) {
                line += pos; // move char ptr past extracted number
                update.push_back(num);
                if (*line == ',') line++;
            }
            
            bool valid_update = true;
            for (int i = 0; i < update.size() && valid_update; i++) {
                const std::set<int> rule_i = rules[update[i]];
                for (int j = i + 1; j < update.size(); j++) {
                    if (rule_i.find(update[j]) == rule_i.end()) {
                        valid_update = false;
                        break;
                    }
                }
                if (!valid_update) break;
            }
            if (valid_update) total += update[((int) update.size()) / 2];
        }
    }
    return PyLong_FromLong(total);
}


// Manual parsing
static PyObject* solve(PyObject *self, PyObject *args) {
    PyObject* page;
    PyArg_ParseTuple(args, "O", &page);
    
    // convert page into Py list
    PyObject* lines = PyUnicode_Splitlines(page, 0);
    Py_ssize_t n_lines = PyList_Size(lines);

    std::map<int, std::set<int> > rules;

    int total = 0;
    bool parsing_rules = true;
    for (Py_ssize_t n = 0; n < n_lines; n++) {
        PyObject *line_obj = PyList_GetItem(lines, n);
        char *line = (char *) PyUnicode_AsUTF8(line_obj);

        if (strcmp(line, "") == 0) {
            parsing_rules = false;
            continue;
        }

        if (parsing_rules) {
            int x = 0, y = 0;

            // Parse first number (x)
            char* ptr = line;
            while (*ptr >= '0' && *ptr <= '9') {
                x = x * 10 + (*ptr - '0');
                ptr++;
            }
            ptr++; // skip '|'
            
            // Parse second number (y)
            while (*ptr >= '0' && *ptr <= '9') {
                y = y * 10 + (*ptr - '0');
                ptr++;
            }
            
            rules[x].insert(y);
        } else {
            std::vector<int> update;

            char* ptr = line;
            while (*ptr) {
                int num = 0;
                // Parse next number
                while (*ptr >= '0' && *ptr <= '9') {
                    num = num * 10 + (*ptr - '0');
                    ptr++;
                }
                update.push_back(num);
                if (*ptr == ',') ptr++;
            }
            
            bool valid_update = true;
            for (int i = 0; i < update.size() && valid_update; i++) {
                const std::set<int> rule_i = rules[update[i]];
                for (int j = i + 1; j < update.size(); j++) {
                    if (rule_i.find(update[j]) == rule_i.end()) {
                        valid_update = false;
                        break;
                    }
                }
                if (!valid_update) break;
            }
            if (valid_update) total += update[((int) update.size()) / 2];
        }
    }
    return PyLong_FromLong(total);
}


// unordered containers -> still a lot of allocating and deallocating
static PyObject* f4(PyObject *self, PyObject *args) {
    PyObject* page;
    PyArg_ParseTuple(args, "O", &page);
    
    // convert page into Py list
    PyObject* lines = PyUnicode_Splitlines(page, 0);
    Py_ssize_t n_lines = PyList_Size(lines);

    std::unordered_map<int, std::unordered_set<int> > rules;

    int total = 0;
    bool parsing_rules = true;
    for (Py_ssize_t n = 0; n < n_lines; n++) {
        PyObject *line_obj = PyList_GetItem(lines, n);
        char *line = (char *) PyUnicode_AsUTF8(line_obj);

        if (strcmp(line, "") == 0) {
            parsing_rules = false;
            continue;
        }

        if (parsing_rules) {
            int x = 0, y = 0;
            char* ptr = line;
            
            // Parse first number (x)
            while (*ptr >= '0' && *ptr <= '9') {
                x = x * 10 + (*ptr - '0');
                ptr++;
            }
            ptr++; // skip '|'
            
            // Parse second number (y)
            while (*ptr >= '0' && *ptr <= '9') {
                y = y * 10 + (*ptr - '0');
                ptr++;
            }
            
            rules[x].insert(y);
        } else {
            std::vector<int> update;
            char* ptr = line;
            
            while (*ptr) {
                int num = 0;
                // Parse next number
                while (*ptr >= '0' && *ptr <= '9') {
                    num = num * 10 + (*ptr - '0');
                    ptr++;
                }
                update.push_back(num);
                if (*ptr == ',') ptr++;
            }
            
            bool valid_update = true;
            for (int i = 0; i < update.size() && valid_update; i++) {
                const std::unordered_set<int> rule_i = rules[update[i]];
                for (int j = i + 1; j < update.size(); j++) {
                    if (rule_i.find(update[j]) == rule_i.end()) {
                        valid_update = false;
                        break;
                    }
                }
                if (!valid_update) break;
            }
            if (valid_update) total += update[((int) update.size()) / 2];
        }
    }
    return PyLong_FromLong(total);
}


// array of array for rules (native C array) [malloc based on n_lines and n_cols]
static PyObject* f6(PyObject *self, PyObject *args) {
    PyObject* page;
    PyArg_ParseTuple(args, "O", &page);
    
    PyObject* lines = PyUnicode_Splitlines(page, 0);
    Py_ssize_t n_lines = PyList_Size(lines);

    const int MAX_DEPS = 100;
    int** rules = (int**) malloc(n_lines * sizeof(int*));
    
    // Initialize each rule's array with zeros
    for (int i = 0; i < n_lines; i++) {
        rules[i] = (int*) calloc(MAX_DEPS, sizeof(int));  // calloc initializes to 0
    }

    int total = 0;
    bool parsing_rules = true;
    for (Py_ssize_t n = 0; n < n_lines; n++) {
        PyObject *line_obj = PyList_GetItem(lines, n);
        char *line = (char *) PyUnicode_AsUTF8(line_obj);

        if (strcmp(line, "") == 0) {
            parsing_rules = false;
            continue;
        }

        if (parsing_rules) {
            int x = 0, y = 0;
            char* ptr = line;
            
            // Parse first number (x)
            while (*ptr >= '0' && *ptr <= '9') {
                x = x * 10 + (*ptr - '0');
                ptr++;
            }
            ptr++; // skip '|'
            
            // Parse second number (y)
            while (*ptr >= '0' && *ptr <= '9') {
                y = y * 10 + (*ptr - '0');
                ptr++;
            }
            
            // Find first empty slot (0) and insert y
            int* rule = rules[x];
            int pos = 0;
            while (rule[pos] != 0) pos++;
            rule[pos] = y;
        } else {
            std::vector<int> update;
            char* ptr = line;
            
            while (*ptr) {
                int num = 0;
                // Parse next number
                while (*ptr >= '0' && *ptr <= '9') {
                    num = num * 10 + (*ptr - '0');
                    ptr++;
                }
                update.push_back(num);
                
                // Skip comma if present
                if (*ptr == ',') ptr++;
            }
            
            bool valid_update = true;
            for (int i = 0; i < update.size() && valid_update; i++) {
                int* rule_i = rules[update[i]];
                
                for (int j = i + 1; j < update.size(); j++) {
                    bool found = false;
                    // Search until we hit a 0 or find the number
                    for (int k = 0; rule_i[k] != 0; k++) {
                        if (rule_i[k] == update[j]) {
                            found = true;
                            break;
                        }
                    }
                    if (!found) {
                        valid_update = false;
                        break;
                    }
                }
                if (!valid_update) break;
            }
            if (valid_update) total += update[((int) update.size()) / 2];
        }
    }

    // Cleanup
    for (int i = 0; i < n_lines; i++) {
        free(rules[i]);
    }
    free(rules);

    return PyLong_FromLong(total);
}


// just assume max number of keys, < 100, so we don't need to malloc anything but get stack memory
static PyObject* f7(PyObject *self, PyObject *args) {
    PyObject* page;
    PyArg_ParseTuple(args, "O", &page);
    
    PyObject* lines = PyUnicode_Splitlines(page, 0);
    Py_ssize_t n_lines = PyList_Size(lines);

    const int MAX_DEPS = 100; // FIXME: for larger depth you get a segmentation fault
    int rules[MAX_DEPS][MAX_DEPS] = {0};

    int total = 0;
    bool parsing_rules = true;
    for (Py_ssize_t n = 0; n < n_lines; n++) {
        PyObject *line_obj = PyList_GetItem(lines, n);
        char *line = (char *) PyUnicode_AsUTF8(line_obj);

        if (strcmp(line, "") == 0) {
            parsing_rules = false;
            continue;
        }

        if (parsing_rules) {
            int x = 0, y = 0;
            char* ptr = line;
            
            // Parse first number (x)
            while (*ptr >= '0' && *ptr <= '9') {
                x = x * 10 + (*ptr - '0');
                ptr++;
            }
            ptr++; // skip '|'
            
            // Parse second number (y)
            while (*ptr >= '0' && *ptr <= '9') {
                y = y * 10 + (*ptr - '0');
                ptr++;
            }
            
            // Find first empty slot (0) and insert y
            int* rule = rules[x];
            int pos = 0;
            while (rule[pos] != 0) pos++;
            rule[pos] = y;
        } else {
            std::vector<int> update;
            char* ptr = line;
            
            while (*ptr) {
                int num = 0;
                // Parse next number
                while (*ptr >= '0' && *ptr <= '9') {
                    num = num * 10 + (*ptr - '0');
                    ptr++;
                }
                update.push_back(num);
                
                // Skip comma if present
                if (*ptr == ',') ptr++;
            }
            
            bool valid_update = true;
            for (int i = 0; i < update.size() && valid_update; i++) {
                int* rule_i = rules[update[i]];
                
                for (int j = i + 1; j < update.size(); j++) {
                    bool found = false;
                    // Search until we hit a 0 or find the number
                    for (int k = 0; rule_i[k] != 0; k++) {
                        if (rule_i[k] == update[j]) {
                            found = true;
                            break;
                        }
                    }
                    if (!found) {
                        valid_update = false;
                        break;
                    }
                }
                if (!valid_update) break;
            }
            if (valid_update) total += update[((int) update.size()) / 2];
        }
    }
    return PyLong_FromLong(total);
}


// input to string
static PyObject* f8(PyObject *self, PyObject *args) {
    char *page;
    PyArg_ParseTuple(args, "s", &page);

    const int MAX_DEPS = 100;
    int rules[MAX_DEPS][MAX_DEPS] = {0};

    int total = 0;
    bool parsing_rules = true;
    char *page_start = page;
    while (*page_start != '\0') {

        char *page_ptr = page_start;
        int line_length = 0;
        while (*page_ptr != '\n' && *page_ptr != '\0') {
            line_length++;
            page_ptr++;
        }        
        char *line = page_start;
        page_start += line_length;
        
        // Store the original character before modifying it
        char original_char = *page_start;
        if (*page_start == '\n') {
            *page_start = '\0'; // set to line ending so that line is a proper string
            page_start++;
        } else { break; }

        if (strcmp(line, "") == 0) {
            parsing_rules = false;
            *(page_start - 1) = original_char;
            continue;
        }

        if (parsing_rules) {
            int x = 0, y = 0;
            char* ptr = line;
            
            // Parse first number (x)
            while (*ptr >= '0' && *ptr <= '9') {
                x = x * 10 + (*ptr - '0');
                ptr++;
            }
            ptr++; // skip '|'
            
            // Parse second number (y)
            while (*ptr >= '0' && *ptr <= '9') {
                y = y * 10 + (*ptr - '0');
                ptr++;
            }
            
            // Find first empty slot (0) and insert y
            int* rule = rules[x];
            int pos = 0;
            while (rule[pos] != 0) pos++;
            rule[pos] = y;
        } else {
            int update[50] = {0};  // Fixed-size array initialized to zero
            int update_size = 0;   // Track number of elements
            char* ptr = line;
            
            while (*ptr) {
                int num = 0;
                // Parse next number
                while (*ptr >= '0' && *ptr <= '9') {
                    num = num * 10 + (*ptr - '0');
                    ptr++;
                }
                update[update_size++] = num;  // Add number and increment size
                
                // Skip comma if present
                if (*ptr == ',') ptr++;
            }
            
            bool valid_update = true;
            for (int i = 0; i < update_size && valid_update; i++) {
                int* rule_i = rules[update[i]];
                
                for (int j = i + 1; j < update_size; j++) {
                    bool found = false;
                    // Search until we hit a 0 or find the number
                    for (int k = 0; rule_i[k] != 0; k++) {
                        if (rule_i[k] == update[j]) {
                            found = true;
                            break;
                        }
                    }
                    if (!found) {
                        valid_update = false;
                        break;
                    }
                }
                if (!valid_update) break;
            }
            if (valid_update) total += update[update_size / 2];
        }

        // Restore the original character
        *(page_start - 1) = original_char;
    }
    return PyLong_FromLong(total);
}


// vector to array
static PyObject* f9(PyObject *self, PyObject *args) {
    char *page;
    PyArg_ParseTuple(args, "s", &page);

    const int MAX_DEPS = 100;
    int rules[MAX_DEPS][MAX_DEPS] = {0};

    int total = 0;
    bool parsing_rules = true;
    char *page_start = page;
    while (*page_start != '\0') {

        char *page_ptr = page_start;
        int line_length = 0;
        while (*page_ptr != '\n' && *page_ptr != '\0') {
            line_length++;
            page_ptr++;
        }        
        char *line = page_start;
        page_start += line_length;
        
        // Store the original character before modifying it
        char original_char = *page_start;
        if (*page_start == '\n') {
            *page_start = '\0';
            page_start++;
        } else { break; }

        if (strcmp(line, "") == 0) {
            parsing_rules = false;
            *(page_start - 1) = original_char;
            continue;
        }

        if (parsing_rules) {
            int x = 0, y = 0;
            char* ptr = line;
            
            // Parse first number (x)
            while (*ptr >= '0' && *ptr <= '9') {
                x = x * 10 + (*ptr - '0');
                ptr++;
            }
            ptr++; // skip '|'
            
            // Parse second number (y)
            while (*ptr >= '0' && *ptr <= '9') {
                y = y * 10 + (*ptr - '0');
                ptr++;
            }
            
            // Find first empty slot (0) and insert y
            int* rule = rules[x];
            int pos = 0;
            while (rule[pos] != 0) pos++;
            rule[pos] = y;
        } else {
            int update[50] = {0};  // Fixed-size array initialized to zero
            int update_size = 0;   // Track number of elements
            char* ptr = line;
            
            while (*ptr) {
                int num = 0;
                // Parse next number
                while (*ptr >= '0' && *ptr <= '9') {
                    num = num * 10 + (*ptr - '0');
                    ptr++;
                }
                update[update_size++] = num;  // Add number and increment size
                
                // Skip comma if present
                if (*ptr == ',') ptr++;
            }
            
            bool valid_update = true;
            for (int i = 0; i < update_size && valid_update; i++) {
                int* rule_i = rules[update[i]];
                
                for (int j = i + 1; j < update_size; j++) {
                    bool found = false;
                    // Search until we hit a 0 or find the number
                    for (int k = 0; rule_i[k] != 0; k++) {
                        if (rule_i[k] == update[j]) {
                            found = true;
                            break;
                        }
                    }
                    if (!found) {
                        valid_update = false;
                        break;
                    }
                }
                if (!valid_update) break;
            }
            if (valid_update) total += update[update_size / 2];
        }

        // Restore the original character
        *(page_start - 1) = original_char;
    }
    return PyLong_FromLong(total);
}


/*
TODO: tried a couple more things (after compiler args)
- smaller types
- improving branch prediction
- array flattening
- faster number parsing
- 

*/

// smaller types + Compiler args -> smaller types is more conversion
static PyObject* f10(PyObject *self, PyObject *args) {
    char *page;
    PyArg_ParseTuple(args, "s", &page);

    const uint8_t MAX_DEPS = 100;  // Changed to uint8_t since it's < 256
    // Using uint8_t (0-255) since numbers are 2 digits (0-99)
    uint8_t rules[MAX_DEPS][MAX_DEPS] = {0};

    uint32_t total = 0;  // Keep total as uint32_t since it could grow large
    bool parsing_rules = true;
    char *page_start = page;
    while (*page_start != '\0') {

        // TODO: explain
        char *page_ptr = page_start;
        int line_length = 0;
        while (*page_ptr != '\n' && *page_ptr != '\0') {
            line_length++;
            page_ptr++;
        }        
        char *line = page_start;
        page_start += line_length;
        
        // Store the original character before modifying it
        char original_char = *page_start;
        if (*page_start == '\n') {
            *page_start = '\0'; // PLAN set to line ending so that line is a proper string --> alter in place
            page_start++;
        } else { break; }

        if (strcmp(line, "") == 0) {
            parsing_rules = false;
            *(page_start - 1) = original_char;
            continue;
        }

        if (parsing_rules) {
            uint8_t x = 0, y = 0;  // Changed to uint8_t
            char* ptr = line;
            
            // Parse first number (x)
            while (*ptr >= '0' && *ptr <= '9') {
                x = x * 10 + (*ptr - '0');
                ptr++;
            }
            ptr++; // skip '|'
            
            // Parse second number (y)
            while (*ptr >= '0' && *ptr <= '9') {
                y = y * 10 + (*ptr - '0');
                ptr++;
            }
            
            // Find first empty slot (0) and insert y
            uint8_t* rule = rules[x];
            uint8_t pos = 0;  // Changed to uint8_t
            while (rule[pos] != 0) pos++;
            rule[pos] = y;
        } else {
            uint8_t update[50] = {0};  // Changed to uint8_t
            uint8_t update_size = 0;   // Changed to uint8_t
            char* ptr = line;
            
            while (*ptr) {
                uint8_t num = 0;  // Changed to uint8_t
                while (*ptr >= '0' && *ptr <= '9') {
                    num = num * 10 + (*ptr - '0');
                    ptr++;
                }
                update[update_size++] = num;
                
                // Skip comma if present
                if (*ptr == ',') ptr++;
            }
            
            bool valid_update = true;
            for (uint8_t i = 0; i < update_size && valid_update; i++) {
                uint8_t* rule_i = rules[update[i]];
                
                for (uint8_t j = i + 1; j < update_size; j++) {
                    bool found = false;
                    for (uint8_t k = 0; rule_i[k] != 0; k++) {
                        if (rule_i[k] == update[j]) {
                            found = true;
                            break;
                        }
                    }
                    if (!found) {
                        valid_update = false;
                        break;
                    }
                }
                if (!valid_update) break;
            }
            if (valid_update) total += update[update_size / 2];
        }

        // Restore the original character
        *(page_start - 1) = original_char;
    }
    return PyLong_FromLong(total);
}


// array flattening
static PyObject* f11(PyObject *self, PyObject *args) {
    char *page;
    PyArg_ParseTuple(args, "s", &page);

    const int MAX_DEPS = 100;
    // Flattened 2D array to 1D - access with [x * MAX_DEPS + y]
    int rules[MAX_DEPS * MAX_DEPS] = {0};

    int total = 0;
    bool parsing_rules = true;
    char *page_start = page;
    while (*page_start != '\0') {

        char *page_ptr = page_start;
        int line_length = 0;
        while (*page_ptr != '\n' && *page_ptr != '\0') {
            line_length++;
            page_ptr++;
        }        
        char *line = page_start;
        page_start += line_length;
        
        char original_char = *page_start;
        if (*page_start == '\n') {
            *page_start = '\0';
            page_start++;
        } else { break; }

        if (strcmp(line, "") == 0) {
            parsing_rules = false;
            *(page_start - 1) = original_char;
            continue;
        }

        if (parsing_rules) {
            int x = 0, y = 0;
            char* ptr = line;
            
            while (*ptr >= '0' && *ptr <= '9') {
                x = x * 10 + (*ptr - '0');
                ptr++;
            }
            ptr++;
            
            while (*ptr >= '0' && *ptr <= '9') {
                y = y * 10 + (*ptr - '0');
                ptr++;
            }
            
            // Find first empty slot (0) and insert y in flattened array
            int pos = 0;
            while (rules[x * MAX_DEPS + pos] != 0) pos++;
            rules[x * MAX_DEPS + pos] = y;
        } else {
            int update[50] = {0};
            int update_size = 0;
            char* ptr = line;
            
            while (*ptr) {
                int num = 0;
                while (*ptr >= '0' && *ptr <= '9') {
                    num = num * 10 + (*ptr - '0');
                    ptr++;
                }
                update[update_size++] = num;
                
                if (*ptr == ',') ptr++;
            }
            
            bool valid_update = true;
            for (int i = 0; i < update_size && valid_update; i++) {
                // Access flattened array using offset
                const int* rule_i = &rules[update[i] * MAX_DEPS];
                
                for (int j = i + 1; j < update_size; j++) {
                    bool found = false;
                    for (int k = 0; rule_i[k] != 0; k++) {
                        if (rule_i[k] == update[j]) {
                            found = true;
                            break;
                        }
                    }
                    if (!found) {
                        valid_update = false;
                        break;
                    }
                }
                if (!valid_update) break;
            }
            if (valid_update) total += update[update_size / 2];
        }

        *(page_start - 1) = original_char;
    }
    return PyLong_FromLong(total);
}





static PyMethodDef Methods[] = {
    {"solve_cpp", f, METH_VARARGS, "Function"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef Module = {
    PyModuleDef_HEAD_INIT,
    "aoc_cpp",
    NULL,
    -1,
    Methods
};

PyMODINIT_FUNC PyInit_aoc_cpp(void) {
    return PyModule_Create(&Module);
}
