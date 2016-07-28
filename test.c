#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
    int c;
    FILE *file, *output;
    if (argc < 2) {
        printf("Usage of ./test: ./test <input file>\n");
        return 0;
    }
    file = fopen(argv[1], "r");

    // Format name of output file.
    const char * suffix = ".ad.c";
    char * dot;
    int needed = strlen(argv[1]) + strlen(suffix) + 1;
    char store[needed];
    strcpy(store, argv[1]);

    // Format for printing output to newly named file.
    dot = strchr(store, '.');
    if (dot != 0) {
        *dot = 0;
    }
    strcat(store, suffix);

    output = fopen(store, "w+");
    if (file) {
        while ((c = getc(file)) != EOF)
            fputc(c, output);
        fprintf(output, "\n}");
        fprintf(stdout, "Success on running ./test, input.ad.c generated.\n");
    } else {
        printf("File does not exist.\n");
        return 0;
    }
    fclose(file);
    fclose(output);
    return 0;
}