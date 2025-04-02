#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include <ctype.h>
#include <string.h>

#define ALPHA 26

bool ispangram(char *s) {
  int c, arr[ALPHA];

  while ((c = *(s++)) != '\0') {
    if (isalpha(c)) {
      arr[tolower(c) - 'a'] = 1;
    }
  }
  
  for (int i = 0; i < ALPHA; i++) {
      if (arr[i] != 1) {
          return false;
      }
      else { /* printf("%c = %d\n", i + 'a', arr[i]); */ }
  }
  return true;
}

int main() {
  size_t len;
  ssize_t read;
  char *line = NULL;
  /*
  read = getline(&line, &len, stdin);
  if (ispangram(line)) {
      printf("%s", line);
  }
  */
  
  int count = 0; 
  while ((read = getline(&line, &len, stdin)) != -1) {
      if (ispangram(line)) {
          count++; 
          printf("%s", line);
      }
      else { 
      }
  }
  printf("%d", count);

  if (ferror(stdin))
    fprintf(stderr, "Error reading from stdin");

  free(line);
  fprintf(stderr, "ok\n");
}
