#!/usr/bin/env python3
import csv
import matplotlib.pyplot as plt
import numpy as np

CSV_FILE = "./tests/fuzzing_results.csv"

def safe_int(value):
    """Converte para int, retorna None se for -1 ou inválido."""
    try:
        val = int(value)
        return None if val == -1 else val
    except (ValueError, TypeError):
        return None

# Ler dados do CSV
data = []
with open(CSV_FILE, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        data.append(row)

print(f"Total de registros: {len(data)}")

# Preparar dados e filtrar casos onde O0 falhou (-1)
case_data = []
for idx, row in enumerate(data, start=1):
    instr_o0 = safe_int(row.get('Instr_O0', '-1'))
    # Desconsiderar casos onde O0 falhou (Instr_O0 = -1)
    if instr_o0 is not None:
        case_info = {
            'index': idx,
            'instr_o0': instr_o0,
            'instr_o2': safe_int(row.get('Instr_O2', '-1')),
            'instr_o3': safe_int(row.get('Instr_O3', '-1')),
            'instr_tiny': safe_int(row.get('Instr_TinyO0', '-1')),
            'same_exit': safe_int(row.get('SameExitCode', '0')) == 1
        }
        case_data.append(case_info)

print(f"Casos válidos (O0 não falhou): {len(case_data)}")

# ===== GRÁFICO 1: Média de instruções removidas de cada compilador =====
print("\n=== Gerando gráfico 1: Média de instruções removidas ===")

# Calcular número absoluto de instruções removidas comparando O0 com cada compilador
# Comparações: O0 vs O2, O0 vs O3, O0 vs TinyO0
reductions = {
    'O2': [],      # O0 - O2
    'O3': [],      # O0 - O3
    'TinyO0': []   # O0 - TinyO0
}

for c in case_data:
    instr_o0 = c['instr_o0']
    # Comparação O0 vs O2
    if c['instr_o2'] is not None:
        reduction = instr_o0 - c['instr_o2']
        reductions['O2'].append(reduction)
    # Comparação O0 vs O3
    if c['instr_o3'] is not None:
        reduction = instr_o0 - c['instr_o3']
        reductions['O3'].append(reduction)
    # Comparação O0 vs TinyO0
    if c['instr_tiny'] is not None:
        reduction = instr_o0 - c['instr_tiny']
        reductions['TinyO0'].append(reduction)

# Calcular médias e medianas das reduções para cada compilador
means = []
medians = []
labels = []
counts = []
for label in ['O2', 'O3', 'TinyO0']:
    if reductions[label]:
        mean = np.mean(reductions[label])
        median = np.median(reductions[label])
        means.append(mean)
        medians.append(median)
        labels.append(label)
        counts.append(len(reductions[label]))

if means:
    fig1 = plt.figure(figsize=(10, 6))
    positions = np.arange(len(labels))
    # Usar mediana em vez de média (mais robusta a outliers)
    bars = plt.bar(positions, medians)
    plt.ylabel('Mediana de Instruções Removidas')
    plt.xlabel('Compilador')
    plt.title('Mediana de Instruções Removidas por Compilador (em relação a O0)')
    plt.xticks(positions, labels)
    plt.grid(axis='y', alpha=0.3)
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # Adicionar valores nas barras com informação do número de casos
    for bar, median, count in zip(bars, medians, counts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{median:.1f}\n(n={count})',
                ha='center', va='bottom' if median > 0 else 'top',
                fontweight='bold', fontsize=9)
    
    # Debug: imprimir valores
    print("Valores calculados (mediana):")
    for label, median, count in zip(labels, medians, counts):
        print(f"  {label}: mediana = {median:.2f} instruções removidas (n={count} casos)")
    print("\nValores calculados (média - para referência):")
    for label, mean, count in zip(labels, means, counts):
        print(f"  {label}: média = {mean:.2f} instruções removidas (n={count} casos)")
    
    plt.tight_layout()
    plt.savefig('./tests/grafico_media_instrucoes_removidas.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Gráfico salvo: grafico_media_instrucoes_removidas.png")

# ===== GRÁFICO 2: Comparação de número de instruções dos 20 primeiros casos =====
print("\n=== Gerando gráfico 2: Comparação dos 20 primeiros casos ===")

# Pegar primeiros 20 casos válidos (com todos os dados)
valid_first20 = []
for c in case_data[:19]:
    if (c['instr_o0'] is not None and c['instr_o2'] is not None and 
        c['instr_o3'] is not None and c['instr_tiny'] is not None):
        valid_first20.append(c)

if valid_first20:
    fig2 = plt.figure(figsize=(14, 8))
    x = np.arange(len(valid_first20))
    width = 0.2
    
    instr_o0_vals = [c['instr_o0'] for c in valid_first20]
    instr_o2_vals = [c['instr_o2'] for c in valid_first20]
    instr_o3_vals = [c['instr_o3'] for c in valid_first20]
    instr_tiny_vals = [c['instr_tiny'] for c in valid_first20]
    
    plt.bar(x - 1.5*width, instr_o0_vals, width, label='O0')
    plt.bar(x - 0.5*width, instr_o2_vals, width, label='O2')
    plt.bar(x + 0.5*width, instr_o3_vals, width, label='O3')
    plt.bar(x + 1.5*width, instr_tiny_vals, width, label='TinyO0')
    
    plt.xlabel('Caso')
    plt.ylabel('Número de Instruções')
    plt.title('Comparação de Número de Instruções: 20 Primeiros Casos')
    plt.xticks(x, [c['index'] for c in valid_first20], rotation=45, ha='right')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('./tests/grafico_comparacao_20_primeiros.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Gráfico salvo: grafico_comparacao_20_primeiros.png")

# ===== GRÁFICO 3: Dispersão de instruções removidas (TinyOpt e O0) =====
print("\n=== Gerando gráfico 3: Dispersão de instruções removidas ===")

# Coletar dados válidos (O0 e TinyO0)
valid_pairs = []
for c in case_data:
    if c['instr_o0'] is not None and c['instr_tiny'] is not None:
        valid_pairs.append((c['instr_o0'], c['instr_tiny']))

if valid_pairs:
    instr_o0_vals, instr_tiny_vals = zip(*valid_pairs)
    
    fig3 = plt.figure(figsize=(8, 8))
    plt.scatter(instr_o0_vals, instr_tiny_vals, alpha=0.6)
    
    # Linha diagonal (y=x) para referência
    max_val = max(max(instr_o0_vals), max(instr_tiny_vals))
    plt.plot([0, max_val], [0, max_val], 'r--', label='y=x (sem redução)', linewidth=2)
    
    plt.xlabel('Instruções O0')
    plt.ylabel('Instruções TinyO0')
    plt.title('Dispersão: Instruções O0 vs TinyO0')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('./tests/grafico_dispersao_instrucoes_tinyopt_o0.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Gráfico salvo: grafico_dispersao_instrucoes_tinyopt_o0.png")

# ===== GRÁFICO 4: Pizza com preservação de semântica do TinyOpt =====
print("\n=== Gerando gráfico 4: Preservação de semântica ===")

preserved_count = sum(1 for c in case_data if c['same_exit'])
total_count = len(case_data)
not_preserved_count = total_count - preserved_count

if total_count > 0:
    preserved_rate = (preserved_count / total_count) * 100
    not_preserved_rate = 100 - preserved_rate
    
    fig4 = plt.figure(figsize=(8, 8))
    plt.pie([preserved_rate, not_preserved_rate],
            labels=['Preservado', 'Não Preservado'],
            autopct='%1.1f%%',
            startangle=90)
    plt.title(f'Preservação de Semântica - TinyOpt\n{preserved_count}/{total_count} casos preservados')
    plt.tight_layout()
    plt.savefig('./tests/grafico_pizza_preservacao_semantica.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Gráfico salvo: grafico_pizza_preservacao_semantica.png")

print("\n=== Todos os gráficos gerados com sucesso! ===")

