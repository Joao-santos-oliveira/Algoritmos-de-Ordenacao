"""
plot_time.py
Lê os arquivos .dat gerados pelo programa (criar_output),
gera um CSV consolidado e 9 gráficos de tempo de execução:
  - 3 gráficos: por algoritmo (comparando 5 linguagens)
  - 5 gráficos: por linguagem (comparando 3 algoritmos)
  - 1 gráfico combinado: 3 subplots lado a lado (um por algoritmo)

Uso:
    python plot_time.py --dir outputs
    python comparacoes/plot_time.py --dir outputs --salvar --saida comparacoes/tempo_graficos
"""

import os
import re
import csv
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from collections import defaultdict

# ─── Configuração ─────────────────────────────────────────────────────────────

# Mapeamento de n por nome de input (ajuste conforme seus arquivos de input)
INPUT_N = {
    "input1": 100,
    "input2": 1_000,
    "input3": 10_000,
    "input4": 100_000,
    "input5": 1_000_000,
    "input6": 10_000_000,
}

ALGORITMOS = ["Radix Sort", "Counting Sort", "Introsort"]
LINGUAGENS = ["C", "C++", "GO", "Haskell", "RUST"]

# Chaves internas (como aparecem nos .dat)
ALGO_KEY = {
    "Radix Sort":    "RADIX",
    "Counting Sort": "COUNTING",
    "Introsort":     "INTROSORT",
}
LANG_KEY = {
    "C":       "C",
    "C++":     "CPP",
    "Go":      "GO",
    "Haskell": "Haskell",
    "Rust":    "RUST",
}

# Paleta por linguagem
LANG_COLOR = {
    "C":       "#E85D04",
    "C++":     "#2563EB",
    "GO":      "#00ADD8",
    "Haskell": "#8B5CF6",
    "RUST":    "#B91C1C",
}

# Paleta por algoritmo
ALGO_COLOR = {
    "Radix Sort":    "#2563EB",
    "Counting Sort": "#16A34A",
    "Introsort":     "#D97706",
}

LANG_MARKER = {
    "C": "o", "C++": "s", "GO": "^", "Haskell": "D", "RUST": "P"
}

LANG_LABEL = {
    "C": "C", "C++": "C++", "GO": "Go", "Haskell": "Haskell", "RUST": "Rust"
}

ALGO_MARKER = {
    "Radix Sort": "o", "Counting Sort": "s", "Introsort": "^"
}

# ─── Parsing ──────────────────────────────────────────────────────────────────

def _extrair_n(input_path: str) -> int | None:
    """
    Tenta extrair n de duas formas:
    1. Lê o arquivo de input diretamente (primeira linha = quantidade)
    2. Infere pelo nome do arquivo (input1 → 100, etc.)
    """
    # Tenta leitura direta
    try:
        with open(input_path.strip(), "r") as f:
            return int(f.readline().strip())
    except (FileNotFoundError, ValueError):
        pass

    # Fallback: infere pelo nome
    nome = os.path.splitext(os.path.basename(input_path.strip()))[0].lower()
    for chave, n in INPUT_N.items():
        if chave in nome:
            return n

    return None

def _extrair_tempos(linhas: list[str]) -> list[float]:
    tempos = []
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        # captura qualquer número incluindo notação científica: 1.04137e-4, 9.8241e-5
        m = re.search(r":\s*([+-]?\d+\.?\d*[eE][+-]?\d+|\d+\.?\d*)", linha)
        if m:
            try:
                tempos.append(float(m.group(1)))
            except ValueError:
                pass
    return tempos

def carregar_dados(diretorio: str) -> list[dict]:
    """
    Lê todos os .dat do diretório e retorna lista de dicts:
      {algoritmo, linguagem, input_n, tempo_medio, tempo_min, tempo_max, arquivo}
    """
    registros = []
    erros = []

    arquivos = sorted(f for f in os.listdir(diretorio) if f.endswith(".dat"))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo .dat encontrado em '{diretorio}'.")

    for nome in arquivos:
        caminho = os.path.join(diretorio, nome)
        try:
            with open(caminho, "r", errors="replace") as f:
                linhas = f.readlines()

            if len(linhas) < 4:
                erros.append(f"⚠ {nome}: arquivo muito curto")
                continue

            linguagem  = linhas[0].split(":", 1)[1].strip()
            algoritmo  = linhas[1].split(":", 1)[1].strip()
            input_path = linhas[2].split(":", 1)[1].strip()
            # linha 3 = cabeçalho "Tempos de execução..."
            tempos_brutos = _extrair_tempos(linhas[4:])

            if not tempos_brutos:
                erros.append(f"⚠ {nome}: nenhum tempo válido encontrado")
                continue

            n = _extrair_n(input_path)
            if n is None:
                erros.append(f"⚠ {nome}: não foi possível determinar n a partir de '{input_path}'")
                continue

            if (algoritmo.lower() == "intro sort" or algoritmo.lower() == "introsort sort"):
                algoritmo = "Introsort"
            
            registros.append({
                "algoritmo":   algoritmo,
                "linguagem":   linguagem,
                "input_n":     n,
                "tempo_medio": sum(tempos_brutos) / len(tempos_brutos),
                "tempo_min":   min(tempos_brutos),
                "tempo_max":   max(tempos_brutos),
                "execucoes":   len(tempos_brutos),
                "arquivo":     nome,
            })

        except Exception as e:
            erros.append(f"✗ {nome}: {e}")

    if erros:
        print("Avisos ao carregar arquivos:")
        for msg in erros:
            print(f"  {msg}")
        print()

    if not registros:
        raise RuntimeError("Nenhum registro válido foi carregado.")

    return registros


# ─── CSV ──────────────────────────────────────────────────────────────────────

def salvar_csv(registros: list[dict], caminho: str) -> None:
    campos = ["algoritmo", "linguagem", "input_n",
              "tempo_medio", "tempo_min", "tempo_max", "execucoes", "arquivo"]
    with open(caminho, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(registros)
    print(f"✔ CSV salvo em: {caminho}")


# ─── Helpers de formatação ────────────────────────────────────────────────────

def _fmt_n(n: float) -> str:
    n = int(n)
    if n >= 1_000_000: return f"{n//1_000_000}M"
    if n >= 1_000:     return f"{n//1_000}k"
    return str(n)


def _fmt_tempo(t: float, _=None) -> str:
    if t is None:  return "—"
    if t < 1e-6:   return f"{t*1e9:.1f} ns"
    if t < 1e-3:   return f"{t*1e6:.1f} µs"
    if t < 1:      return f"{t*1e3:.2f} ms"
    return f"{t:.3f} s"


# ─── Helpers de plot ──────────────────────────────────────────────────────────

def _estilo_base(ax, titulo: str, ylabel: bool = True) -> None:
    ax.set_facecolor("#0F172A")
    ax.set_title(titulo, fontsize=12, fontweight="bold", color="white", pad=10)
    ax.set_xlabel("Número de entradas (n)", fontsize=10, color="#94A3B8", labelpad=6)
    if ylabel:
        ax.set_ylabel("Tempo médio de execução", fontsize=10, color="#94A3B8", labelpad=6)
    ax.tick_params(colors="#94A3B8", labelsize=8)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: _fmt_n(x)))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(_fmt_tempo))
    for spine in ax.spines.values():
        spine.set_edgecolor("#1E293B")
    ax.grid(True, which="major", color="#1E293B", linewidth=0.7)
    ax.grid(True, which="minor", color="#1E293B", linewidth=0.3, linestyle=":")


def _legenda(ax) -> None:
    leg = ax.legend(fontsize=8.5, framealpha=0.85,
                    facecolor="#1E293B", edgecolor="#334155",
                    labelcolor="white", fancybox=False, loc="upper left")
    leg.get_frame().set_linewidth(0.8)


def _anotar(ax, ns, ts, cor) -> None:
    for n, t in zip(ns, ts):
        ax.annotate(_fmt_tempo(t),
                    xy=(n, t), xytext=(4, 4),
                    textcoords="offset points",
                    fontsize=6.5, color=cor, alpha=0.75)


def _agrupar(registros: list[dict], chave1: str, chave2: str) -> dict:
    """Agrupa: dados[chave1][chave2] = {n: tempo_medio}"""
    dados = defaultdict(lambda: defaultdict(dict))
    for r in registros:
        dados[r[chave1]][r[chave2]][r["input_n"]] = r["tempo_medio"]
    return dados


# ─── Gráficos por algoritmo (compara linguagens) ──────────────────────────────

def graficos_por_algoritmo(registros: list[dict], salvar: bool, out_dir: str) -> None:
    dados = _agrupar(registros, "algoritmo", "linguagem")

    for algo in ALGORITMOS:
        fig, ax = plt.subplots(figsize=(9, 5.5))
        fig.patch.set_facecolor("#0F172A")

        for lang in LINGUAGENS:
            pts = dados[algo].get(lang, {})
            if not pts:
                continue
            ns = sorted(pts)
            ts = [pts[n] for n in ns]
            ax.plot(ns, ts,
                    marker=LANG_MARKER.get(lang, "o"), markersize=7,
                    linewidth=2, color=LANG_COLOR.get(lang, "#FFFFFF"),
                    label=LANG_LABEL.get(lang, lang), zorder=3)
            _anotar(ax, ns, ts, LANG_COLOR.get(lang, "#FFFFFF"))

        ax.set_xscale("log")
        ax.set_yscale("log")
        _estilo_base(ax, f"Tempo de execução — {algo}")
        _legenda(ax)
        plt.tight_layout()

        chave = ALGO_KEY.get(algo, algo.upper().replace(" ", "_"))
        caminho = os.path.join(out_dir, f"tempo_{chave.lower()}.png")
        if salvar:
            fig.savefig(caminho, dpi=150, bbox_inches="tight",
                        facecolor=fig.get_facecolor())
            print(f"  ✔ {caminho}")
        else:
            plt.show()
        plt.close(fig)


# ─── Gráficos por linguagem (compara algoritmos) ──────────────────────────────

def graficos_por_linguagem(registros: list[dict], salvar: bool, out_dir: str) -> None:
    dados = _agrupar(registros, "linguagem", "algoritmo")

    for lang in LINGUAGENS:
        fig, ax = plt.subplots(figsize=(9, 5.5))
        fig.patch.set_facecolor("#0F172A")

        for algo in ALGORITMOS:
            pts = dados[lang].get(algo, {})
            if not pts:
                continue
            ns = sorted(pts)
            ts = [pts[n] for n in ns]
            ax.plot(ns, ts,
                    marker=ALGO_MARKER.get(algo, "o"), markersize=7,
                    linewidth=2, color=ALGO_COLOR.get(algo, "#FFFFFF"),
                    label=algo, zorder=3)
            _anotar(ax, ns, ts, ALGO_COLOR.get(algo, "#FFFFFF"))

        ax.set_xscale("log")
        ax.set_yscale("log")
        _estilo_base(ax, f"Tempo de execução — {lang}")
        _legenda(ax)
        plt.tight_layout()

        chave = LANG_KEY.get(lang, lang.upper())
        caminho = os.path.join(out_dir, f"tempo_{chave.lower()}.png")
        if salvar:
            fig.savefig(caminho, dpi=150, bbox_inches="tight",
                        facecolor=fig.get_facecolor())
            print(f"  ✔ {caminho}")
        else:
            plt.show()
        plt.close(fig)


# ─── Gráfico combinado: 3 subplots (um por algoritmo) ────────────────────────

def grafico_combinado_algoritmos(registros: list[dict], salvar: bool, out_dir: str) -> None:
    dados = _agrupar(registros, "algoritmo", "linguagem")

    fig, axes = plt.subplots(1, 3, figsize=(22, 6), sharey=False)
    fig.patch.set_facecolor("#0F172A")
    fig.suptitle("Tempo de execução por método de ordenação — comparação entre linguagens",
                 fontsize=14, fontweight="bold", color="white", y=1.02)

    for ax, algo in zip(axes, ALGORITMOS):
        ax.set_facecolor("#0F172A")

        for lang in LINGUAGENS:
            pts = dados[algo].get(lang, {})
            if not pts:
                continue
            ns = sorted(pts)
            ts = [pts[n] for n in ns]
            ax.plot(ns, ts,
                    marker=LANG_MARKER.get(lang, "o"), markersize=7,
                    linewidth=2, color=LANG_COLOR.get(lang, "#FFFFFF"),
                    label=lang, zorder=3)

        ax.set_xscale("log")
        ax.set_yscale("log")
        _estilo_base(ax, algo, ylabel=(algo == ALGORITMOS[0]))
        _legenda(ax)

    plt.tight_layout()
    caminho = os.path.join(out_dir, "tempo_algoritmos_combinado.png")
    if salvar:
        fig.savefig(caminho, dpi=150, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        print(f"  ✔ {caminho}")
    else:
        plt.show()
    plt.close(fig)


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gerador de gráficos de tempo para benchmarks de ordenação."
    )
    parser.add_argument("--dir",    default="outputs",
                        help="Pasta com os arquivos .dat (padrão: outputs)")
    parser.add_argument("--csv",    default="comparacoes/tempo_graficos/tempo_benchmarks.csv",
                        help="Caminho do CSV de saída")
    parser.add_argument("--salvar", action="store_true",
                        help="Salva PNGs em vez de exibir")
    parser.add_argument("--saida",  default="comparacoes/tempo_graficos",
                        help="Pasta para salvar os PNGs")
    args = parser.parse_args()

    print(f"Lendo .dat em: {args.dir}")
    registros = carregar_dados(args.dir)
    print(f"  {len(registros)} registros carregados\n")

    salvar_csv(registros, args.csv)

    os.makedirs(args.saida, exist_ok=True)

    print("\nGerando gráficos por algoritmo (comparando linguagens):")
    graficos_por_algoritmo(registros, args.salvar, args.saida)

    print("\nGerando gráficos por linguagem (comparando algoritmos):")
    graficos_por_linguagem(registros, args.salvar, args.saida)

    print("\nGerando gráfico combinado (3 subplots por algoritmo):")
    grafico_combinado_algoritmos(registros, args.salvar, args.saida)

    print(f"\n✔ 9 gráficos gerados em '{args.saida}'")


if __name__ == "__main__":
    main()