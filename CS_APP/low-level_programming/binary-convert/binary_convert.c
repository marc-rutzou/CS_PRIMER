int binary_convert(char *bits) {
    char c;
    int n = 0;
    while ((c = *bits++) != '\0') {
        n <<= 1;
        n += c - '0';
    }
    return n;
}
