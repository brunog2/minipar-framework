#ifndef MINIPAR_RT_H
#define MINIPAR_RT_H

#include <pthread.h>

void minipar_channel_create(const char *type, const char *name, const char *args);
void minipar_channel_send(const char *name, double value);
double minipar_channel_recv(const char *name);
void minipar_par_begin(void);
void minipar_par_end(int n_threads);
void minipar_thread_begin(int id);
void minipar_thread_end(int id);

#endif
