const IMPRIMIR_LISTA: bool = false;

fn adquirir_maior_valor(lista: &[i32]) -> i32 {
    let mut maior = lista[0];
    for &num in lista.iter() {
        if num > maior {
            maior = num;
        }
    }
    maior
}

fn counting_sort_simplificado(lista: &[i32], lista_aux: &mut Vec<i32>, exp: i32) -> Vec<i32> {
    let mut count = vec![0i32; 10];

    for &num in lista.iter() {
        count[((num / exp) % 10) as usize] += 1;
    }

    for i in 1..10 {
        count[i] += count[i - 1];
    }

    for i in (0..lista.len()).rev() {
        let digito = ((lista[i] / exp) % 10) as usize;
        lista_aux[count[digito] as usize - 1] = lista[i];
        count[digito] -= 1;
    }

    lista_aux.to_vec()
}

// Radix Sort LSD
pub fn radix_sort(lista: &[i32]) -> Vec<i32> {
    let mut lista_atual: Vec<i32> = lista.to_vec();
    let mut lista_auxiliar: Vec<i32> = vec![0; lista.len()];

    let maior_valor = adquirir_maior_valor(lista);
    let mut expo: i32 = 1;

    if IMPRIMIR_LISTA {
        println!("Lista original: {:?}", lista);
    }

    while maior_valor / expo > 0 {
        lista_atual = counting_sort_simplificado(&lista_atual, &mut lista_auxiliar, expo);
        expo *= 10;
    }

    if IMPRIMIR_LISTA {
        println!("Lista ordenada: {:?}", lista_atual);
    }

    lista_atual
}