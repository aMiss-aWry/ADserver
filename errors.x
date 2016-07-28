The BTO server was unable to compile and generate an output file.
Args: ['/lighthouse/src/BTOServer/test.c', '--delete_tmp', '-e']
Exception: [Errno 2] No such file or directory
--- BEGIN output from test ---
1
---  END output from test  ---

Generated .m file used in call:
#include <stdio.h>

int main()
{
    int c;
    FILE *file, *output;
    file = fopen("input.c", "r");
    output = fopen("input.ad.c", "w+");
    if (file) {
        while ((c = getc(file)) != EOF)
            fputc(c, output);
    }
    fprintf(output, "\n}");
    fclose(file);
    fclose(output);
    fprintf(stdout, "Success on running ./test\n" );
    return 0;
}