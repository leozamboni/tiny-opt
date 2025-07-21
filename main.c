#include <stdio.h>

int yyparse(void);

int main() {
    printf("Digite o código C:\n");
    yyparse();
    return 0;
}
