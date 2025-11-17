#!/usr/bin/env bash

FUZZ_DIR="./fuzzing"
TMP_DIR="./tmp"
OUT_DIR="./bin"
CSV_FILE="./tests/fuzzing_results.csv"

echo "==> Verificando dependências..."

check_bin() {
    name="$1"
    cmd="$2"
    if command -v "$cmd" >/dev/null 2>&1; then
        echo "[OK] $name encontrado: $cmd"
    else
        echo "[AVISO] $name NÃO encontrado! ($cmd)"
        exit 1 
    fi
}

check_bin "GCC" gcc
check_bin "OBJDUMP" objdump

if [[ -x "./tinyopt" ]]; then
    echo "[OK] TinyOpt encontrado ./tinyopt"
else
    echo "[AVISO] TinyOpt NÃO encontrado em ./tinyopt"
fi

echo ""

mkdir -p "$TMP_DIR"
mkdir -p "$OUT_DIR"

echo "Index;SameExitCode;Instr_O0;Instr_O2;Instr_O3;Instr_TinyO0" > "$CSV_FILE"

index=0

count_instr() {
    bin="$1"
    if [[ -f "$bin" ]] && command -v objdump >/dev/null; then
        objdump -d "$bin" 2>/dev/null | grep '^[[:space:]]*[0-9a-f]\+:' | wc -l
    else
        echo -1
    fi
}

for src in "$FUZZ_DIR"/*.c; do
    index=$((index + 1))
    base=$(basename "$src" .c)

    echo "==> Testando $base.c"

    # 1) gcc -O0
    gcc -O0 "$src" -o "$OUT_DIR/${base}_O0.bin" 2>/dev/null
    exit_O0=$?
    bin_O0="$OUT_DIR/${base}_O0.bin"
    [[ $exit_O0 -ne 0 ]] && bin_O0="/dev/null"

    # 2) tinyopt
    ./tinyopt < "$src" > "$TMP_DIR/${base}_opt.c" 2>/dev/null

    # 3) tinyopt → gcc -O0
    gcc -O0 "$TMP_DIR/${base}_opt.c" -o "$OUT_DIR/${base}_tinyO0.bin" 2>/dev/null
    exit_tinyO0=$?
    bin_tiny="$OUT_DIR/${base}_tinyO0.bin"
    [[ $exit_tinyO0 -ne 0 ]] && bin_tiny="/dev/null"

    # 4) gcc -O2
    gcc -O2 "$src" -o "$OUT_DIR/${base}_O2.bin" 2>/dev/null
    bin_O2="$OUT_DIR/${base}_O2.bin"
    [[ ! -f "$bin_O2" ]] && bin_O2="/dev/null"

    # 5) gcc -O3
    gcc -O3 "$src" -o "$OUT_DIR/${base}_O3.bin" 2>/dev/null
    bin_O3="$OUT_DIR/${base}_O3.bin"
    [[ ! -f "$bin_O3" ]] && bin_O3="/dev/null"

    # 7) instruções
    count_O0=$(count_instr "$bin_O0")
    count_O2=$(count_instr "$bin_O2")
    count_O3=$(count_instr "$bin_O3")
    count_tinyO0=$(count_instr "$bin_tiny")

    # 10) comparação de exit
    same_exit=0
    [[ "$exit_O0" -eq "$exit_tinyO0" ]] && same_exit=1

    # 11) CSV
    echo "$index;$same_exit;$count_O0;$count_O2;$count_O3;$count_TCC;$count_tinyO0;$size_O0;$size_O2;$size_O3;$size_TCC;$size_tinyO0;$time_O0;$time_O2;$time_O3;$time_TCC;$time_tinyO0" >> "$CSV_FILE"

done

echo "Finalizado. CSV gerado em $CSV_FILE"
