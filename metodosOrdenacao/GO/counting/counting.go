package counting

func CountingSort(lista []int) {

	var tamanho int = len(lista)
	var maior_valor int = adquirirMaiorValor(lista)

	count := make([]int, maior_valor+1)

	for i := 0; i < tamanho; i++ {
		count[lista[i]]++
	}
	for i := 1; i < maior_valor+1; i++ {
		count[i] += count[i-1]
	}

	aux := make([]int, tamanho)

	for i := tamanho - 1; i > -1; i-- {
		valor := lista[i]
		aux[count[valor]-1] = valor
		count[valor]--
	}
	for i := 0; i < tamanho; i++ {
		lista[i] = aux[i]
	}
}

func adquirirMaiorValor(lista []int) int {

	var tamanho int = len(lista)
	var maior int = lista[0]

	for i := 0; i < tamanho; i++ {
		if lista[i] > maior {
			maior = lista[i]
		}
	}
	return maior

}
