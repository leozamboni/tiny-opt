all:
	bison -d parser.y
	flex lexer.l
	gcc -std=c11 -D_GNU_SOURCE -o tinyopt parser.tab.c lex.yy.c main.c ast.c optimizer.c codegen.c cfg.c -lm

clean:
	rm -f tinyopt parser.tab.* lex.yy.c