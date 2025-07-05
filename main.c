#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>

#define MAX_LINE 1024
#define MAX_ARGS 64

void execute(char **args) {
    pid_t pid = fork();
    if (pid == 0) {
        execvp(args[0], args);
        perror("mysh");
        exit(EXIT_FAILURE);
    } else {
        wait(NULL);
    }
}

char **parse_input(char *line) {
    char **args = malloc(MAX_ARGS * sizeof(char *));
    int i = 0;
    char *token = strtok(line, " \t\n");
    while (token != NULL) {
        args[i++] = token;
        token = strtok(NULL, " \t\n");
    }
    args[i] = NULL;
    return args;
}

int main() {
    char line[MAX_LINE];
    char **args;

    while (1) {
        fflush(stdout);
        if (!fgets(line, MAX_LINE, stdin)) break;

        args = parse_input(line);
        if (args[0] == NULL) {
            printf("__PROMPT__\n");
            fflush(stdout);
            free(args);
            continue;
        }

        if (strcmp(args[0], "exit") == 0) {
            free(args);
            break;
        }

        execute(args);
        free(args);

        printf("__PROMPT__\n");
        fflush(stdout);
    }
    return 0;
}