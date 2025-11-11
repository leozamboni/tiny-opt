CC = gcc
CFLAGS = -std=c99 -D_GNU_SOURCE -Wall -Wextra
SRC = parser.tab.c lex.yy.c main.c ast.c optimizer.c codegen.c cfg.c
OUT = tinyopt

all: parser lex $(OUT)

parser: parser.y
	bison -d parser.y

lex: lexer.l
	flex lexer.l

$(OUT): $(SRC)
	$(CC) $(CFLAGS) -o $(OUT) $(SRC) -lm

format:
	@indent -gnu *.c *.h 

clean:
	rm -f $(OUT) parser.tab.* lex.yy.c
	rm -f *.c~ *.h~ 
