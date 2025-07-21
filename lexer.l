%{
#include "parser.tab.h"
#include <string.h>
%}

digit       [0-9]
letter      [a-zA-Z_]
id          {letter}({letter}|{digit})*
number      {digit}+(\.{digit}+)?([eE][+-]?{digit}+)?

%%

"int"           { return INT; }
"float"         { return FLOAT; }
"return"        { return RETURN; }

{number}        {
                    yylval.str = strdup(yytext);
                    return NUMBER;
                }

{id}            {
                    yylval.str = strdup(yytext);
                    return ID;
                }

"+"             { return '+'; }
"-"             { return '-'; }
"*"             { return '*'; }
"/"             { return '/'; }
"="             { return '='; }
";"             { return ';'; }

[ \t\r\n]+      { /* ignorar */ }

.               { printf("Caractere inválido: %s\n", yytext); return yytext[0]; }

%%

int yywrap(void) { return 1; }
