mod problema;
mod counting;
mod introsort;
mod radix;

use problema::*;
use counting::counting_sort;
use introsort::intro_sort;
use radix::radix_sort;
use std::time::Instant;

// Altere para ESCOLHER_EM_EXECUCAO ou para os enums de Algoritmos
const ALGORITMO_USADO: i32 = ESCOLHER_EM_EXECUCAO;

// Altere para ESCOLHER_EM_EXECUCAO ou para um numero correspondente ao numero do input
const INPUT_USADO: i32 = ESCOLHER_EM_EXECUCAO;

// Altere para ESCOLHER_EM_EXECUCAO ou para um numero correspondente ao numero de execucoes
// Serve para calcular o tempo médio do algoritmo
const QUANTIDADE_EXECUCOES: i32 = ESCOLHER_EM_EXECUCAO;

// 0 - Falso, 1 - Verdadeiro
const EXIBIR_INFORMACOES: i32 = 0;

fn executar_algoritmo(
    prob: &Problema,
    func_algoritmo: fn(&[i32]) -> Vec<i32>,
) {
    let mut lista_tempos = Vec::with_capacity(prob.quantidade_execucoes as usize);
    let lista_principal = &prob.lista;

    for i in 0..prob.quantidade_execucoes {
        if EXIBIR_INFORMACOES != 0 {
            println!("\nExecução {} em andamento...", i + 1);
        }

        let start = Instant::now();
        let _ = func_algoritmo(lista_principal);
        let elapsed = start.elapsed().as_secs_f64();

        lista_tempos.push(elapsed);

        if EXIBIR_INFORMACOES != 0 {
            println!(
                "Execução {} concluída. Tempo gasto: {} segundos.",
                i + 1,
                elapsed
            );
        }
    }

    criar_output(prob, &lista_tempos);
}

// Wrapper para intro_sort (adaptação de interface)
fn intro_sort_wrapper(lista: &[i32]) -> Vec<i32> {
    let mut result = lista.to_vec();
    intro_sort(&mut result);
    result
}



fn main() {
    let mut problema = criar_problema(INPUT_USADO, ALGORITMO_USADO, QUANTIDADE_EXECUCOES);

    match problema.algoritmo_usado {
        RADIX_SORT => executar_algoritmo(&problema, radix_sort),
        COUNTING_SORT => executar_algoritmo(&problema, counting_sort),
        INTRO_SORT => executar_algoritmo(&problema, intro_sort_wrapper),
        TODOS => {
            problema.algoritmo_usado = RADIX_SORT;
            executar_algoritmo(&problema, radix_sort);

            problema.algoritmo_usado = COUNTING_SORT;
            executar_algoritmo(&problema, counting_sort);

            problema.algoritmo_usado = INTRO_SORT;
            executar_algoritmo(&problema, intro_sort_wrapper);
        }
        _ => println!("Algoritmo não implementado."),
    }

    println!("Algoritmos finalizados com sucesso...");
}