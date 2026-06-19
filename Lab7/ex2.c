#define OPENSSL_SUPPRESS_DEPRECATED
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <openssl/sha.h>
#include <time.h>

#define ITERS 2000000

unsigned long stretch_hash(const char* path) {
    FILE* f = fopen(path, "r");
    if (!f) return 0;
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);
    unsigned char* buf = malloc(sz);
    fread(buf, 1, sz, f);
    fclose(f);
    unsigned char digest[32];
    SHA256_CTX ctx;
    SHA256_Init(&ctx);
    SHA256_Update(&ctx, buf, sz);
    SHA256_Final(digest, &ctx);
    free(buf);
    for (int i = 0; i < ITERS; i++) {
        SHA256_Init(&ctx);
        SHA256_Update(&ctx, digest, 32);
        SHA256_Final(digest, &ctx);
    }
    unsigned long sum = 0;
    for (int i = 0; i < 32; i++)
        sum += digest[i];
    return sum;
}

int num_files;
char** file_names;
unsigned long* results;

int current_file = 0;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void* worker_routine(void* arg) {
    while (1) {
        int index = -1;
        pthread_mutex_lock(&mutex);
        if (current_file < num_files) {
            index = current_file++;
        }
        pthread_mutex_unlock(&mutex);
        
        if (index == -1) break;
        
        results[index] = stretch_hash(file_names[index]);
        printf("Processed %s\n", file_names[index]);
    }
    return NULL;
}

int main(int argc, char** argv) {
    if (argc < 3) {
        printf("Usage: %s <num_threads> <file1> <file2> ...\n", argv[0]);
        return 1;
    }
    
    int num_threads = atoi(argv[1]);
    num_files = argc - 2;
    file_names = &argv[2];
    results = calloc(num_files, sizeof(unsigned long));
    
    pthread_t* threads = malloc(num_threads * sizeof(pthread_t));
    
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < num_threads; i++) {
        pthread_create(&threads[i], NULL, worker_routine, NULL);
    }
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }
    
    clock_gettime(CLOCK_MONOTONIC, &end);
    double elapsed = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    printf("Processing time: %.4f seconds\n", elapsed);
    
    free(threads);
    free(results);
    return 0;
}
