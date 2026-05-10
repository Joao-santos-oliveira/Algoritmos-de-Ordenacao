package radix

const (
	IMPRIMIR_LISTA = false
)

func adquirir_maior_valor(lista []int) int {
	maior := lista[0]
	for i := 1; i < len(lista); i++ {
		if lista[i] > maior {
			maior = lista[i]
		}
	}

	return maior
}

func counting_sort_simplificado(lista []int, lista_aux []int, exp int) {
	count := make([]int, 10)
	tam := len(lista)
	for i := 0; i < tam; i++ {
		count[(lista[i] / exp) % 10]++
	}

	for i := 1; i < 10; i++ {
		count[i] += count[i-1]
	}

	for i := tam - 1; i >= 0; i-- {
		digito := (lista[i] / exp) % 10
		lista_aux[count[digito]-1] = lista[i]
		count[digito]--
	}

	copy(lista, lista_aux)
}

// Radix Sort LSD
func RadixSort(lista []int) {
	lista_aux := make([]int, len(lista))

	maior_valor := adquirir_maior_valor(lista)
	exp := 1

	if (IMPRIMIR_LISTA) {
		println("Lista antes da ordenação:")
		for v := range lista {
			print(lista[v], ", ")
		}
	}

	for exp = 1; maior_valor/exp > 0; exp *= 10 {
		counting_sort_simplificado(lista, lista_aux, exp)
	}

	if (IMPRIMIR_LISTA) {
		println("\nLista após a ordenação:")
		for v := range lista {
			print(lista[v], ", ")
		}
		println()
	}
}