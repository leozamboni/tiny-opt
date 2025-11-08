int mdc(int a, int b) {
    while (b != 0) {
        int resto = a % b;
        a = b;
        b = resto;
    }
    return a;
}

int main() {
    int x = 1;
    int y = 10;
    return mdc(x, y);
}