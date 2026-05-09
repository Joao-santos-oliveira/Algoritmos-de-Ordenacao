"""
plot_memory.py
Lê os benchmarks de /usr/bin/time -v e Haskell RTS,
gera um CSV consolidado e 8 gráficos de memória:
  - 3 gráficos: por algoritmo (comparando 5 linguagens)
  - 5 gráficos: por linguagem (comparando 3 algoritmos)

Uso:
    python comparacoes/plot_memory.py --dir benchmarks --salvar
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

INPUTS = [100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000]
ALGORITMOS = ["RADIX", "COUNTING", "INTROSORT"]
LINGUAGENS = ["C", "CPP", "GO", "Haskell", "RUST"]

LANG_PREFIX = {
    "C":       "benchmark_c_",
    "CPP":     "benchmark_cpp_",
    "GO":      "benchmark_go_",
    "Haskell": "benchmark_hs_",
    "RUST":    "benchmark_rs_",
}

LANG_LABEL = {
    "C": "C", "CPP": "C++", "GO": "Go", "Haskell": "Haskell", "RUST": "Rust"
}

ALGO_LABEL = {
    "RADIX": "Radix Sort", "COUNTING": "Counting Sort", "INTROSORT": "Introsort"
}

# Paleta distinta por linguagem
LANG_COLOR = {
    "C":       "#E85D04",   # laranja
    "CPP":     "#2563EB",   # azul
    "GO":      "#00ADD8",   # ciano Go
    "Haskell": "#8B5CF6",   # roxo
    "RUST":    "#B91C1C",   # vermelho Rust
}

# Paleta distinta por algoritmo
ALGO_COLOR = {
    "RADIX":    "#2563EB",
    "COUNTING": "#16A34A",
    "INTROSORT":"#D97706",
}

MARKERS = {"C": "o", "CPP": "s", "GO": "^", "Haskell": "D", "RUST": "P"}
ALGO_MARKERS = {"RADIX": "o", "COUNTING": "s", "INTROSORT": "^"}


# ─── Parsing ──────────────────────────────────────────────────────────────────

def parse_time_v(text: str) -> float | None:
    """Extrai Maximum resident set size (kbytes) do /usr/bin/time -v."""
    m = re.search(r"Maximum resident set size \(kbytes\):\s*(\d+)", text)
    return float(m.group(1)) if m else None


def parse_haskell_rts(text: str) -> float | None:
    """Extrai total memory in use (MiB) do Haskell +RTS -s e converte para KB."""
    m = re.search(r"(\d+)\s+MiB total memory in use", text)
    if m:
        return float(m.group(1)) * 1024  # MiB → KB
    # fallback: maximum residency em bytes
    m2 = re.search(r"([\d,]+)\s+bytes maximum residency", text)
    if m2:
        return float(m2.group(1).replace(",", "")) / 1024  # bytes → KB
    return None


def parse_file(path: str, lang: str) -> float | None:
    with open(path, "r", errors="replace") as f:
        text = f.read()
    if lang == "Haskell":
        return parse_haskell_rts(text)
    return parse_time_v(text)


def carregar_dados(base_dir: str) -> list[dict]:
    """
    Retorna lista de dicts:
      {algoritmo, linguagem, input_n, memoria_kb, arquivo}
    Assume que os arquivos de cada (algoritmo, linguagem) estão ordenados
    por timestamp → índice 0 = input[0], índice 1 = input[1], ...
    """
    registros = []

    for algo in ALGORITMOS:
        algo_dir = os.path.join(base_dir, algo)
        if not os.path.isdir(algo_dir):
            print(f"⚠ Pasta não encontrada: {algo_dir}")
            continue

        for lang, prefix in LANG_PREFIX.items():
            arquivos = sorted(
                f for f in os.listdir(algo_dir) if f.startswith(prefix)
            )
            if len(arquivos) != len(INPUTS):
                print(f"⚠ {algo}/{lang}: esperava {len(INPUTS)} arquivos, encontrou {len(arquivos)}")

            for idx, nome in enumerate(arquivos):
                n = INPUTS[idx] if idx < len(INPUTS) else None
                if n is None:
                    continue
                path = os.path.join(algo_dir, nome)
                mem = parse_file(path, lang)
                registros.append({
                    "algoritmo":   algo,
                    "linguagem":   lang,
                    "input_n":     n,
                    "memoria_kb":  mem,
                    "arquivo":     nome,
                })

    return registros


# ─── CSV ──────────────────────────────────────────────────────────────────────

def salvar_csv(registros: list[dict], caminho: str) -> None:
    campos = ["algoritmo", "linguagem", "input_n", "memoria_kb", "arquivo"]
    with open(caminho, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(registros)
    print(f"✔ CSV salvo em: {caminho}")


# ─── Helpers de plot ──────────────────────────────────────────────────────────

def _fmt_n(n: float) -> str:
    n = int(n)
    if n >= 1_000_000: return f"{n//1_000_000}M"
    if n >= 1_000:     return f"{n//1_000}k"
    return str(n)


def _fmt_kb(kb: float, _=None) -> str:
    if kb >= 1024 * 1024: return f"{kb/1024/1024:.1f} GB"
    if kb >= 1024:        return f"{kb/1024:.1f} MB"
    return f"{kb:.0f} KB"


def _estilo_base(ax, titulo: str) -> None:
    ax.set_facecolor("#0F172A")
    ax.set_title(titulo, fontsize=13, fontweight="bold",
                 color="white", pad=12)
    ax.set_xlabel("Número de entradas (n)", fontsize=11,
                  color="#94A3B8", labelpad=8)
    ax.set_ylabel("Memória máxima (RSS)", fontsize=11,
                  color="#94A3B8", labelpad=8)
    ax.tick_params(colors="#94A3B8", labelsize=9)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: _fmt_n(x)))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(_fmt_kb))
    for spine in ax.spines.values():
        spine.set_edgecolor("#1E293B")
    ax.grid(True, which="major", color="#1E293B", linewidth=0.7)
    ax.grid(True, which="minor", color="#1E293B", linewidth=0.3, linestyle=":")


def _legenda(ax) -> None:
    leg = ax.legend(fontsize=9, framealpha=0.85,
                    facecolor="#1E293B", edgecolor="#334155",
                    labelcolor="white", fancybox=False,
                    loc="upper left")
    leg.get_frame().set_linewidth(0.8)


# ─── Gráficos por algoritmo (compara linguagens) ──────────────────────────────

def graficos_por_algoritmo(registros: list[dict], salvar: bool, out_dir: str) -> None:
    # agrupa: dados[algo][lang] = {n: kb}
    dados: dict[str, dict[str, dict[int, float]]] = defaultdict(lambda: defaultdict(dict))
    for r in registros:
        if r["memoria_kb"] is not None:
            dados[r["algoritmo"]][r["linguagem"]][r["input_n"]] = r["memoria_kb"]

    for algo in ALGORITMOS:
        fig, ax = plt.subplots(figsize=(9, 5.5))
        fig.patch.set_facecolor("#0F172A")

        for lang in LINGUAGENS:
            pts = dados[algo].get(lang, {})
            if not pts:
                continue
            ns = sorted(pts)
            ks = [pts[n] for n in ns]
            ax.plot(ns, ks,
                    marker=MARKERS[lang], markersize=7,
                    linewidth=2, color=LANG_COLOR[lang],
                    label=LANG_LABEL[lang], zorder=3)

        ax.set_xscale("log")
        ax.set_yscale("log")
        _estilo_base(ax, f"Uso de memória — {ALGO_LABEL[algo]}")
        _legenda(ax)

        # anotações nos pontos
        for lang in LINGUAGENS:
            pts = dados[algo].get(lang, {})
            for n, kb in pts.items():
                ax.annotate(_fmt_kb(kb),
                            xy=(n, kb), xytext=(4, 4),
                            textcoords="offset points",
                            fontsize=6.5, color=LANG_COLOR[lang], alpha=0.75)

        plt.tight_layout()
        nome = f"memoria_{algo.lower()}.png"
        caminho = os.path.join(out_dir, nome)
        if salvar:
            fig.savefig(caminho, dpi=150, bbox_inches="tight",
                        facecolor=fig.get_facecolor())
            print(f"  ✔ {caminho}")
        else:
            plt.show()
        plt.close(fig)


# ─── Gráficos por linguagem (compara algoritmos) ──────────────────────────────

def graficos_por_linguagem(registros: list[dict], salvar: bool, out_dir: str) -> None:
    dados: dict[str, dict[str, dict[int, float]]] = defaultdict(lambda: defaultdict(dict))
    for r in registros:
        if r["memoria_kb"] is not None:
            dados[r["linguagem"]][r["algoritmo"]][r["input_n"]] = r["memoria_kb"]

    for lang in LINGUAGENS:
        fig, ax = plt.subplots(figsize=(9, 5.5))
        fig.patch.set_facecolor("#0F172A")

        for algo in ALGORITMOS:
            pts = dados[lang].get(algo, {})
            if not pts:
                continue
            ns = sorted(pts)
            ks = [pts[n] for n in ns]
            ax.plot(ns, ks,
                    marker=ALGO_MARKERS[algo], markersize=7,
                    linewidth=2, color=ALGO_COLOR[algo],
                    label=ALGO_LABEL[algo], zorder=3)

        ax.set_xscale("log")
        ax.set_yscale("log")
        _estilo_base(ax, f"Uso de memória — {LANG_LABEL[lang]}")
        _legenda(ax)

        for algo in ALGORITMOS:
            pts = dados[lang].get(algo, {})
            for n, kb in pts.items():
                ax.annotate(_fmt_kb(kb),
                            xy=(n, kb), xytext=(4, 4),
                            textcoords="offset points",
                            fontsize=6.5, color=ALGO_COLOR[algo], alpha=0.75)

        plt.tight_layout()
        nome = f"memoria_{lang.lower()}.png"
        caminho = os.path.join(out_dir, nome)
        if salvar:
            fig.savefig(caminho, dpi=150, bbox_inches="tight",
                        facecolor=fig.get_facecolor())
            print(f"  ✔ {caminho}")
        else:
            plt.show()
        plt.close(fig)


# ─── Gráfico combinado: 3 subplots lado a lado (um por algoritmo) ─────────────

def grafico_combinado_algoritmos(registros: list[dict], salvar: bool, out_dir: str) -> None:
    dados: dict[str, dict[str, dict[int, float]]] = defaultdict(lambda: defaultdict(dict))
    for r in registros:
        if r["memoria_kb"] is not None:
            dados[r["algoritmo"]][r["linguagem"]][r["input_n"]] = r["memoria_kb"]

    fig, axes = plt.subplots(1, 3, figsize=(22, 6), sharey=False)
    fig.patch.set_facecolor("#0F172A")
    fig.suptitle("Uso de memória por método de ordenação — comparação entre linguagens",
                 fontsize=14, fontweight="bold", color="white", y=1.02)

    for ax, algo in zip(axes, ALGORITMOS):
        ax.set_facecolor("#0F172A")

        for lang in LINGUAGENS:
            pts = dados[algo].get(lang, {})
            if not pts:
                continue
            ns = sorted(pts)
            ks = [pts[n] for n in ns]
            ax.plot(ns, ks,
                    marker=MARKERS[lang], markersize=7,
                    linewidth=2, color=LANG_COLOR[lang],
                    label=LANG_LABEL[lang], zorder=3)

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(ALGO_LABEL[algo], fontsize=12, fontweight="bold",
                     color="white", pad=10)
        ax.set_xlabel("Número de entradas (n)", fontsize=10,
                      color="#94A3B8", labelpad=6)
        ax.set_ylabel("Memória máxima (RSS)" if algo == "RADIX" else "",
                      fontsize=10, color="#94A3B8", labelpad=6)
        ax.tick_params(colors="#94A3B8", labelsize=8)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: _fmt_n(x)))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(_fmt_kb))
        for spine in ax.spines.values():
            spine.set_edgecolor("#1E293B")
        ax.grid(True, which="major", color="#1E293B", linewidth=0.7)
        ax.grid(True, which="minor", color="#1E293B", linewidth=0.3, linestyle=":")

        leg = ax.legend(fontsize=8.5, framealpha=0.85,
                        facecolor="#1E293B", edgecolor="#334155",
                        labelcolor="white", fancybox=False, loc="upper left")
        leg.get_frame().set_linewidth(0.8)

    plt.tight_layout()
    nome = "memoria_algoritmos_combinado.png"
    caminho = os.path.join(out_dir, nome)
    if salvar:
        fig.savefig(caminho, dpi=150, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        print(f"  ✔ {caminho}")
    else:
        plt.show()
    plt.close(fig)


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir",    default="benchmarks",
                        help="Pasta raiz com subpastas RADIX/COUNTING/INTROSORT")
    parser.add_argument("--csv",    default="comparacoes/memoria_graficos/memoria_benchmarks.csv",
                        help="Caminho do CSV de saída")
    parser.add_argument("--salvar", action="store_true",
                        help="Salva PNGs em vez de exibir")
    parser.add_argument("--saida",  default="comparacoes/memoria_graficos",
                        help="Pasta para salvar os PNGs")
    args = parser.parse_args()

    print(f"Lendo benchmarks em: {args.dir}")
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