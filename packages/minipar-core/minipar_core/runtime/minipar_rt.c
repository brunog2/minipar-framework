#include "minipar_rt.h"

#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define MAX_CHANNELS 32
#define MAX_THREADS 16

typedef struct {
    char name[64];
    int server_fd;
    int port;
    int is_server;
} MiniParChannel;

static MiniParChannel channels[MAX_CHANNELS];
static int channel_count = 0;
static int par_children = 0;
static int in_child = 0;

static MiniParChannel *find_channel(const char *name) {
    for (int i = 0; i < channel_count; i++) {
        if (strcmp(channels[i].name, name) == 0) {
            return &channels[i];
        }
    }
    return NULL;
}

void minipar_channel_create(const char *type, const char *name, const char *args) {
    (void)args;
    if (channel_count >= MAX_CHANNELS) {
        return;
    }
    MiniParChannel *ch = &channels[channel_count++];
    strncpy(ch->name, name, sizeof(ch->name) - 1);
    ch->is_server = (strcmp(type, "s_channel") == 0);
    if (ch->is_server) {
        ch->server_fd = socket(AF_INET, SOCK_STREAM, 0);
        struct sockaddr_in addr;
        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
        addr.sin_port = 0;
        bind(ch->server_fd, (struct sockaddr *)&addr, sizeof(addr));
        socklen_t len = sizeof(addr);
        getsockname(ch->server_fd, (struct sockaddr *)&addr, &len);
        ch->port = ntohs(addr.sin_port);
        listen(ch->server_fd, 1);
    }
}

void minipar_channel_send(const char *name, double value) {
    MiniParChannel *ch = find_channel(name);
    if (!ch || !ch->is_server) {
        return;
    }
    struct sockaddr_in addr;
    socklen_t len = sizeof(addr);
    getsockname(ch->server_fd, (struct sockaddr *)&addr, &len);
    int client = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in srv;
    memset(&srv, 0, sizeof(srv));
    srv.sin_family = AF_INET;
    srv.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    srv.sin_port = htons(ch->port);
    connect(client, (struct sockaddr *)&srv, sizeof(srv));
    char buf[64];
    snprintf(buf, sizeof(buf), "%.17g\n", value);
    send(client, buf, strlen(buf), 0);
    close(client);
}

double minipar_channel_recv(const char *name) {
    MiniParChannel *ch = find_channel(name);
    if (!ch || !ch->is_server) {
        return 0.0;
    }
    int conn = accept(ch->server_fd, NULL, NULL);
    char buf[64] = {0};
    recv(conn, buf, sizeof(buf) - 1, 0);
    close(conn);
    return atof(buf);
}

void minipar_par_begin(void) {
    par_children = 0;
}

void minipar_thread_begin(int id) {
    (void)id;
    if (in_child) {
        return;
    }
    pid_t pid = fork();
    if (pid == 0) {
        in_child = 1;
    } else if (pid > 0) {
        par_children++;
    }
}

void minipar_thread_end(int id) {
    (void)id;
    if (in_child) {
        exit(0);
    }
}

void minipar_par_end(int n_threads) {
    (void)n_threads;
    for (int i = 0; i < par_children; i++) {
        wait(NULL);
    }
}
