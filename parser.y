%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex(void);
void yyerror(const char *s);

%}

%union {
    char* str;
}

%token <str> ID NUMBER
%token INT FLOAT RETURN

%type <str> expression

%%

program:
    program statement
    | /* vazio */
    ;

statement:
      declaration ';'
    | assignment ';'
    | RETURN expression ';'   { printf("return %s\n", $2); free($2); }
    ;

declaration:
      INT ID         { printf("declaração: int %s\n", $2); free($2); }
    | FLOAT ID       { printf("declaração: float %s\n", $2); free($2); }
    ;

assignment:
    ID '=' expression { printf("atribuição: %s = %s\n", $1, $3); free($1); free($3); }
    ;

expression:
      expression '+' expression { asprintf(&$$, "(%s + %s)", $1, $3); free($1); free($3); }
    | expression '-' expression { asprintf(&$$, "(%s - %s)", $1, $3); free($1); free($3); }
    | expression '*' expression { asprintf(&$$, "(%s * %s)", $1, $3); free($1); free($3); }
    | expression '/' expression { asprintf(&$$, "(%s / %s)", $1, $3); free($1); free($3); }
    | NUMBER                   { $$ = $1; }
    | ID                       { $$ = $1; }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro: %s\n", s);
}
