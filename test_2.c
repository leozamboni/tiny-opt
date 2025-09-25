int n;
int i;
int j;
int t1 = 0;
int t2 = 1;
int nextTerm;
int unused_var;
int dead_store_var;

n = 2 + 3;
i = 10 - 5;
j = 4 * 2 + 1;

unused_var = 100;

dead_store_var = 999;
dead_store_var = 42;

if (5 == 20) {
    n = 10;
}

if (1 == 1) {
    i = i + 1;
} else {
    j = 0;
}

for (i = 0; i < 3; i++) {
    nextTerm = t1 + t2;
    t1 = t2;
    t2 = nextTerm;
}

return t2;
n = 999;
i = 888;