#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

#include <sys/syscall.h>
#include <sys/time.h>
#include <sys/resource.h>

#define SLEEP_SEC 3
#define NUM_MULS 100000000
#define NUM_MALLOCS 100000
#define MALLOC_SIZE 1000

struct profile_times {
    suseconds_t real_time;
    suseconds_t user_time;
    suseconds_t system_time;
};

void profile_start(struct profile_times *t) {
    struct timeval tv;
    syscall(SYS_gettimeofday, &tv, NULL);
    t->real_time = tv.tv_usec; 

    struct rusage ru;
    syscall(SYS_getrusage, RUSAGE_SELF, &ru);
    t->user_time = ru.ru_utime.tv_usec;
    t->system_time = ru.ru_stime.tv_usec;
}

// TODO given starting information, compute and log differences to now
void profile_log(struct profile_times *t) {
    struct timeval tv;
    syscall(SYS_gettimeofday, &tv, NULL);
    printf("real: %ld;", tv.tv_usec - t->real_time);

    struct rusage ru;
    syscall(SYS_getrusage, RUSAGE_SELF, &ru);
    printf("\tuser: %ld;", ru.ru_utime.tv_usec - t->user_time);
    printf("\tsystem: %ld\n", ru.ru_stime.tv_usec - t->system_time);
}

int main(int argc, char *argv[]) {
    struct profile_times t;

    float x = 1.0;
    profile_start(&t);
    for (int i = 0; i < NUM_MULS; i++)
    x *= 1.1;
    profile_log(&t);

    profile_start(&t);
    void *p;
    for (int i = 0; i < NUM_MALLOCS; i++)
    p = malloc(MALLOC_SIZE);
    profile_log(&t);

    profile_start(&t);
    sleep(SLEEP_SEC);
    profile_log(&t);
}
