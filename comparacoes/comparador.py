"""
plot_benchmarks.py
Gerador de gráficos para benchmarks de algoritmos de ordenação.

Uso:
    python plot_benchmarks.py                   # modo padrão (ALGORITMO)
    python plot_benchmarks.py --modo linguagem  # agrupa por linguagem
    python plot_benchmarks.py --modo algoritmo  # agrupa por algoritmo
    python plot_benchmarks.py --modo todos      # uma linha por (linguagem, algoritmo)
    python plot_benchmarks.py --salvar          # salva PNG em vez de exibir
    python plot_benchmarks.py --salvar --modo todos --saida resultado.png
"""

import os
import enum
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from dataclasses import dataclass, field
from collections import defaultdict


# ──────────────────────────────────────────────
# Configuração
# ──────────────────────────────────────────────

DIRETORIO_OUTPUTS = "outputs"

PALETA = [
    "#2563EB",  # azul
    "#DC2626",  # vermelho
    "#16A34A",  # verde
    "#D97706",  # âmbar
    "#7C3AED",  # violeta
    "#0891B2",  # ciano
    "#DB2777",  # rosa
    "#65A30D",  # lima
]

MARCADORES = ["o", "s", "^", "D", "v", "P", "X", "*"]

CURVAS_REF = {
    "O(n)":        lambda n: n,
    "O(n log n)":  lambda n: n * np.log2(np.maximum(n, 2)),
    "O(n²)":       lambda n: n ** 2,
}


class KeyType(enum.Enum):
    LINGUAGEM = "linguagem"
    ALGORITMO = "algoritmo"
    TODOS     = "todos"


# ──────────────────────────────────────────────
# Estruturas de dados
# ──────────────────────────────────────────────

@dataclass
class SerieExecucao:
    """Representa uma curva no gráfico: tempos por tamanho de entrada."""
    label: str
    linguagem: str
    algoritmo: str
    tempos: dict = field(default_factory=dict)   # {n: tempo_medio}


# ──────────────────────────────────────────────
# Parsing
# ──────────────────────────────────────────────

def _ler_quantidade(input_path: str) -> int:
    """Lê o número de elementos do arquivo de input."""
    try:
        with open(input_path, "r") as f:
            return int(f.readline().strip())
    except (FileNotFoundError, ValueError) as e:
        raise RuntimeError(f"Não foi possível ler '{input_path}': {e}") from e


def _chave(linguagem: str, algoritmo: str, modo: KeyType) -> str:
    match modo:
        case KeyType.LINGUAGEM: return linguagem
        case KeyType.ALGORITMO: return algoritmo
        case KeyType.TODOS:     return f"{linguagem} — {algoritmo}"


def carregar_series(diretorio: str, modo: KeyType) -> dict[str, SerieExecucao]:
    """Lê todos os .dat do diretório e retorna um dicionário de séries."""
    series: dict[str, SerieExecucao] = {}
    erros: list[str] = []

    arquivos_dat = sorted(
        f for f in os.listdir(diretorio) if f.endswith(".dat")
    )
    if not arquivos_dat:
        raise FileNotFoundError(f"Nenhum arquivo .dat encontrado em '{diretorio}'.")

    for nome_arq in arquivos_dat:
        caminho = os.path.join(diretorio, nome_arq)
        try:
            with open(caminho, "r") as f:
                linguagem = f.readline().split(":", 1)[1].strip()
                algoritmo = f.readline().split(":", 1)[1].strip()
                input_rel = f.readline().split(":", 1)[1].strip()
                f.readline()  # cabeçalho "Tempos de execução..."

                tempos_brutos: list[float] = []
                for linha in f:
                    linha = linha.strip()
                    if not linha:
                        continue
                    partes = linha.split(":", 1)
                    if len(partes) == 2:
                        try:
                            tempos_brutos.append(float(partes[1].strip()))
                        except ValueError:
                            pass

            if not tempos_brutos:
                erros.append(f"  ⚠  {nome_arq}: nenhuma execução válida encontrada.")
                continue

            n = _ler_quantidade(input_rel)
            tempo_medio = sum(tempos_brutos) / len(tempos_brutos)

            chave = _chave(linguagem, algoritmo, modo)
            if chave not in series:
                label = chave
                series[chave] = SerieExecucao(label=label,
                                               linguagem=linguagem,
                                               algoritmo=algoritmo)
            series[chave].tempos[n] = tempo_medio

        except Exception as e:
            erros.append(f"  ✗  {nome_arq}: {e}")

    if erros:
        print("Avisos ao carregar arquivos:")
        for msg in erros:
            print(msg)
        print()

    if not series:
        raise RuntimeError("Nenhuma série válida foi carregada.")

    return series


# ──────────────────────────────────────────────
# Exibição no terminal
# ──────────────────────────────────────────────

def imprimir_tabela(series: dict[str, SerieExecucao]) -> None:
    col_label = max(len(s.label) for s in series.values())
    todos_n = sorted({n for s in series.values() for n in s.tempos})

    sep = "─" * (col_label + 4 + 14 * len(todos_n))
    cabecalho_n = "".join(f"{'n='+_fmt_n(n):>14}" for n in todos_n)
    print(f"\n{'Série':<{col_label + 4}}{cabecalho_n}")
    print(sep)

    for serie in sorted(series.values(), key=lambda s: s.label):
        linha = f"{serie.label:<{col_label + 4}}"
        for n in todos_n:
            val = serie.tempos.get(n)
            linha += f"{_fmt_tempo(val):>14}"
        print(linha)

    print(sep + "\n")


def _fmt_n(n: int) -> str:
    if n >= 1_000_000:
        return f"{n//1_000_000}M"
    if n >= 1_000:
        return f"{n//1_000}k"
    return str(n)


def _fmt_tempo(t) -> str:
    if t is None:
        return "—"
    if t < 1e-3:
        return f"{t*1e6:.1f} µs"
    if t < 1:
        return f"{t*1e3:.2f} ms"
    return f"{t:.4f} s"


# ──────────────────────────────────────────────
# Gráfico
# ──────────────────────────────────────────────

def _titulo(modo: KeyType, series: dict[str, SerieExecucao]) -> str:
    nomes = sorted({s.algoritmo for s in series.values()})
    match modo:
        case KeyType.LINGUAGEM:
            algos = ", ".join(nomes)
            return f"Comparação de linguagens — {algos}"
        case KeyType.ALGORITMO:
            langs = sorted({s.linguagem for s in series.values()})
            return f"Comparação de algoritmos — {', '.join(langs)}"
        case KeyType.TODOS:
            return "Comparação geral — todos os algoritmos e linguagens"


def _escalar_curva(ns_cont: np.ndarray, func, anchor_n: float, anchor_t: float) -> np.ndarray:
    """
    Escala a curva teórica ancorando num ponto real (anchor_n, anchor_t).
    Garante que a curva passe exatamente por esse ponto nos dados.
    """
    val_na_ancora = func(np.array([anchor_n]))[0]
    if val_na_ancora == 0:
        return func(ns_cont)
    fator = anchor_t / val_na_ancora
    return func(ns_cont) * fator


def gerar_grafico(
    series: dict[str, SerieExecucao],
    modo: KeyType,
    curvas_ref: list[str],
    salvar: str | None = None,
) -> None:

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#F9FAFB")
    ax.set_facecolor("#F9FAFB")

    # ── séries de dados ──
    # Coleta todos os pontos (n, t) para usar na âncora das curvas de referência
    todos_pontos: list[tuple[float, float]] = []
    for idx, serie in enumerate(sorted(series.values(), key=lambda s: s.label)):
        ns = sorted(serie.tempos)
        ts = [serie.tempos[n] for n in ns]
        todos_pontos.extend(zip(ns, ts))

        cor   = PALETA[idx % len(PALETA)]
        marca = MARCADORES[idx % len(MARCADORES)]

        ax.plot(ns, ts,
                marker=marca, markersize=6,
                linewidth=1.8, color=cor,
                label=serie.label, zorder=3)

    # ── curvas de referência ──
    if curvas_ref and todos_pontos:
        todos_n = sorted({n for s in series.values() for n in s.tempos})
        n_min, n_max = todos_n[0], todos_n[-1]
        ns_cont = np.logspace(np.log10(n_min * 0.8), np.log10(n_max * 1.2), 300)

        ref_styles = [
            {"linestyle": ":",  "linewidth": 1.2, "color": "#94A3B8"},
            {"linestyle": "--", "linewidth": 1.2, "color": "#94A3B8"},
            {"linestyle": "-.", "linewidth": 1.2, "color": "#94A3B8"},
        ]

        # Âncora: menor n disponível, menor tempo entre todas as séries nesse n
        n_min_dados = min(n for s in series.values() for n in s.tempos)
        tempos_no_n_min = [
            s.tempos[n_min_dados]
            for s in series.values()
            if n_min_dados in s.tempos
        ]
        anchor_n = float(n_min_dados)
        anchor_t = min(tempos_no_n_min)

        for i, nome in enumerate(curvas_ref):
            func = CURVAS_REF[nome]
            ys = _escalar_curva(ns_cont, func, anchor_n, anchor_t)
            estilo = ref_styles[i % len(ref_styles)]
            ax.plot(ns_cont, ys, label=nome, alpha=0.65, zorder=2, **estilo)

    # ── estética ──
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Quantidade de elementos (n)", fontsize=12, labelpad=8)
    ax.set_ylabel("Tempo médio de execução (s)", fontsize=12, labelpad=8)
    ax.set_title(_titulo(modo, series), fontsize=13, fontweight="bold", pad=14)

    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: _fmt_n(int(x)))
    )
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda y, _: _fmt_tempo(y))
    )

    ax.grid(True, which="major", linestyle="-",  linewidth=0.5, color="#CBD5E1", alpha=0.8)
    ax.grid(True, which="minor", linestyle=":",  linewidth=0.3, color="#CBD5E1", alpha=0.5)
    ax.tick_params(axis="both", labelsize=10)

    for spine in ax.spines.values():
        spine.set_edgecolor("#CBD5E1")

    leg = ax.legend(
        fontsize=10, framealpha=0.92,
        edgecolor="#CBD5E1", fancybox=False,
        loc="upper left",
    )
    leg.get_frame().set_linewidth(0.5)

    plt.tight_layout()

    if salvar:
        fig.savefig(salvar, dpi=150, bbox_inches="tight")
        print(f"Gráfico salvo em: {salvar}")
    else:
        plt.show()

    plt.close(fig)


# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gerador de gráficos para benchmarks de ordenação."
    )
    parser.add_argument(
        "--modo",
        choices=["linguagem", "algoritmo", "todos"],
        default="algoritmo",
        help="Como agrupar as séries (padrão: algoritmo)",
    )
    parser.add_argument(
        "--dir",
        default=DIRETORIO_OUTPUTS,
        metavar="DIRETORIO",
        help=f"Pasta com os .dat (padrão: '{DIRETORIO_OUTPUTS}')",
    )
    parser.add_argument(
        "--ref",
        nargs="*",
        choices=list(CURVAS_REF.keys()),
        default=["O(n)", "O(n log n)"],
        help="Curvas de referência teóricas a exibir",
    )
    parser.add_argument(
        "--salvar",
        metavar="ARQUIVO.png",
        default=None,
        help="Salvar o gráfico como PNG em vez de exibir",
    )
    parser.add_argument(
        "--sem-tabela",
        action="store_true",
        help="Não imprimir a tabela de resultados no terminal",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    modo = KeyType(args.modo)

    print(f"Carregando arquivos de '{args.dir}' | modo: {modo.value}")
    series = carregar_series(args.dir, modo)
    print(f"{len(series)} série(s) carregada(s).\n")

    if not args.sem_tabela:
        imprimir_tabela(series)

    gerar_grafico(
        series=series,
        modo=modo,
        curvas_ref=args.ref or [],
        salvar=args.salvar,
    )


if __name__ == "__main__":
    main()