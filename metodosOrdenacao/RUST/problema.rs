use std::fs::File;
use std::io::{BufRead, BufReader, Write};
use std::process;
use std::time::{SystemTime, UNIX_EPOCH};

pub const ESCOLHER_EM_EXECUCAO: i32 = 0;
pub const RADIX_SORT: i32 = 1;
pub const COUNTING_SORT: i32 = 2;
pub const INTRO_SORT: i32 = 3;
pub const TODOS: i32 = 4;

pub const INPUT1: &str = "inputs/input1.dat";
pub const INPUT2: &str = "inputs/input2.dat";
pub const INPUT3: &str = "inputs/input3.dat";
pub const INPUT4: &str = "inputs/input4.dat";
pub const INPUT5: &str = "inputs/input5.dat";
pub const INPUT6: &str = "inputs/input6.dat";

#[derive(Clone)]
pub struct Problema {
    pub lista: Vec<i32>,
    pub tamanho: usize,
    pub nome_input: String,
    pub algoritmo_usado: i32,
    pub quantidade_execucoes: i32,
}

pub fn ler_input(prob: &mut Problema, filename: &str) {
    let file = File::open(filename).unwrap_or_else(|_| {
        println!("\x1b[31m Erro ao abrir o arquivo.");
        println!(" Arquivo não encontrado ou inacessível: {} \x1b[0m", filename);
        process::exit(1);
    });

    let reader = BufReader::new(file);
    let mut lines = reader.lines();

    // Lê o tamanho
    let tamanho: usize = lines
        .next()
        .unwrap()
        .unwrap()
        .trim()
        .parse()
        .unwrap();

    prob.tamanho = tamanho;
    prob.lista = Vec::with_capacity(tamanho);

    // Lê TODOS os números (independente de linha)
    for line in lines {
        if let Ok(linha) = line {
            let numeros = linha
                .split_whitespace()
                .filter_map(|s| s.parse::<i32>().ok());

            prob.lista.extend(numeros);
        }
    }
}

pub fn obter_nome_input(input: i32) -> String {
    if input == ESCOLHER_EM_EXECUCAO {
        loop {
            println!(" Escolha o Input a ser usado:");
            println!("1. Input 1\n2. Input 2\n3. Input 3\n4. Input 4\n5. Input 5\n6. Input 6");
            print!("Resposta: ");
            std::io::Write::flush(&mut std::io::stdout()).unwrap();

            let mut input_str = String::new();
            std::io::stdin().read_line(&mut input_str).unwrap();
            let choice: i32 = input_str.trim().parse().unwrap_or(0);

            if choice >= 1 && choice <= 6 {
                return get_nome_input(choice);
            } else {
                println!("\n \x1b[31m Opção inválida. Por favor, escolha um número entre 1 e 6. \x1b[0m \n");
            }
        }
    } else {
        get_nome_input(input)
    }
}

fn get_nome_input(input: i32) -> String {
    match input {
        1 => INPUT1.to_string(),
        2 => INPUT2.to_string(),
        3 => INPUT3.to_string(),
        4 => INPUT4.to_string(),
        5 => INPUT5.to_string(),
        6 => INPUT6.to_string(),
        _ => INPUT1.to_string(),
    }
}

pub fn obter_algoritmo_usado(algoritmo: i32) -> i32 {
    if algoritmo == ESCOLHER_EM_EXECUCAO {
        loop {
            println!("\n Escolha o algoritmo:");
            println!("1. Radix\n2. Counting\n3. intro Sort\n4. Todos");
            print!("Resposta: ");
            std::io::Write::flush(&mut std::io::stdout()).unwrap();

            let mut input_str = String::new();
            std::io::stdin().read_line(&mut input_str).unwrap();
            let choice: i32 = input_str.trim().parse().unwrap_or(0);

            if choice >= 1 && choice <= 4 {
                return choice;
            } else {
                println!("\n \x1b[31m Opção inválida.\x1b[0m\n");
            }
        }
    } else {
        algoritmo
    }
}

pub fn obter_quantidade_execucoes(quantidade_execucoes: i32) -> i32 {
    if quantidade_execucoes == ESCOLHER_EM_EXECUCAO {
        loop {
            print!("\n Digite a quantidade de execuções (1 ou mais): ");
            std::io::Write::flush(&mut std::io::stdout()).unwrap();

            let mut input_str = String::new();
            std::io::stdin().read_line(&mut input_str).unwrap();
            let choice: i32 = input_str.trim().parse().unwrap_or(0);

            if choice >= 1 {
                return choice;
            } else {
                println!("\n \x1b[31m Quantidade inválida.\x1b[0m\n");
            }
        }
    } else {
        quantidade_execucoes
    }
}

pub fn criar_problema(input: i32, algoritmo: i32, quantidade_execucoes: i32) -> Problema {
    let nome_input = obter_nome_input(input);
    let algoritmo_usado = obter_algoritmo_usado(algoritmo);
    let quantidade_execucoes_obtida = obter_quantidade_execucoes(quantidade_execucoes);

    let mut prob = Problema {
        lista: Vec::new(),
        tamanho: 0,
        nome_input: nome_input.clone(),
        algoritmo_usado,
        quantidade_execucoes: quantidade_execucoes_obtida,
    };

    ler_input(&mut prob, &nome_input);

    prob
}

pub fn criar_output(prob: &Problema, lista_tempos: &[f64]) {
    let nome_algoritmo = match prob.algoritmo_usado {
        RADIX_SORT => "Radix Sort",
        COUNTING_SORT => "Counting Sort",
        INTRO_SORT => "introsort Sort",
        _ => "Desconhecido",
    };

    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();

    let nome_arquivo = format!("outputs/output{}.dat", timestamp);

    let mut file = File::create(&nome_arquivo).unwrap_or_else(|_| {
        println!("Erro ao criar o arquivo de saída.");
        process::exit(1);
    });

    writeln!(file, "Linguagem: RUST").unwrap();
    writeln!(file, "Algoritmo: {}", nome_algoritmo).unwrap();
    writeln!(file, "Input: {}", prob.nome_input).unwrap();
    writeln!(file, "Tempos de execução (em segundos):").unwrap();

    for (i, tempo) in lista_tempos.iter().enumerate() {
        writeln!(file, "Execução {}: {}", i, tempo).unwrap();
    }
}

/*
pub fn exibir_lista(lista: &[i32]) {
    for (i, &item) in lista.iter().enumerate() {
        if i < lista.len() - 1 {
            print!("{}, ", item);
        } else {
            println!("{}", item);
        }
    }
}
*/