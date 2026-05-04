pub fn counting_sort(lista: &mut [i32]) {

    let tamanho: usize = lista.len();
    let maior_valor: i32 = adquirir_maior_valor(lista);

    let mut count = vec![0;maior_valor  as usize +1];
    for i in 0..tamanho {
        count[lista[i]  as usize] += 1;
    }
    for i in 1..(maior_valor  as usize +1){
        count[i] += count[i-1];
    }

    let mut aux = vec![0;tamanho];

    for i in (0..tamanho).rev() {
        let valor = lista[i];
        aux[count[valor as usize] - 1] = valor;
        count[valor as usize] -= 1;
    }
    for i in 0..tamanho {
        lista[i] = aux[i];
    }

}

fn adquirir_maior_valor(lista: &[i32]) -> i32{
    let mut maior: i32 = lista[0];
    for i in 1..lista.len() {
        if lista[i] > maior {
			maior = lista[i];
		}
    }
    return maior;
}