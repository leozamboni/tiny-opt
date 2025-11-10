#ifndef OPTIMIZER_H
#define OPTIMIZER_H

#include "ast.h"

typedef enum {
    VALUE_TYPE_UNKNOWN,
    VALUE_TYPE_INT,
    VALUE_TYPE_STRING,
} ValueType;

typedef struct {
    char *str;
    int number;
    ValueType type;
} SymbolValue;

typedef struct SymbolTable {
    char *name;
    char *scope;
    SymbolValue *value;
    uint64_t loop_hash;
    uint64_t id_hash;
    struct SymbolTable *next;
    ASTNode *node;
} SymbolTable;

void optimize_code(ASTNode *ast);

void remove_dead_code(ASTNode *node);
void set_symtab(ASTNode *node, SymbolTable **head, SymbolTable **tail, uint64_t loop_hash, char *scope);

void constant_folding(ASTNode *node);
void reachability_analysis(ASTNode *node, SymbolTable *table, char *current_scope);
void liveness_dse(SymbolTable *table);
void empty_blocks(ASTNode *node);

int has_return_statement(ASTNode *node);
int has_break_continue(ASTNode *node);

void print_optimization_report(ASTNode *ast);

#endif 



















