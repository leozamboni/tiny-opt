all:
	bison -d parser.y
	flex lexer.l
	gcc -std=c99 -o comp parser.tab.c lex.yy.c main.c -lm

clean:
	rm -f comp parser.tab.* lex.yy.c