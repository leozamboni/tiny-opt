int add(int a, int b) {
    return a + b;
}

int get_sum(int x, int y) {
    int r = add(x, y);
    return r;
}

int main() {
    int a = 10;
    int b = 20;
    int c = 30;
    return get_sum(a, b);
}

