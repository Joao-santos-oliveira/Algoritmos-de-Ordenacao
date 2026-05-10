package main

import (
	"fmt"
	"math/rand"
	"time"
	"go_project/radix"
	"go_project/counting"
	"go_project/introsort"
)

// Configurações
const ALGORITMO_USADO = ESCOLHER_EM_EXECUCAO
const INPUT_USADO = ESCOLHER_EM_EXECUCAO
const QUANTIDADE_EXECUCOES = ESCOLHER_EM_EXECUCAO
const EXIBIR_INFORMACOES = 0

func executarAlgoritmo(prob *Problema, funcAlgoritmo func([]int)) {
	listaTempos := make([]float64, prob.QuantidadeExecucoes)
	listaPrincipal := prob.Lista
	tamanho := prob.Tamanho

	listaSecundaria := make([]int, tamanho)

	for i := 0; i < prob.QuantidadeExecucoes; i++ {
		// ✅ cópia correta (built-in)
		copy(listaSecundaria, listaPrincipal)

		if EXIBIR_INFORMACOES != 0 {
			fmt.Printf("\nExecução %d em andamento...\n", i+1)
		}

		start := time.Now()
		funcAlgoritmo(listaSecundaria)
		elapsed := time.Since(start).Seconds()

		listaTempos[i] = elapsed

		if EXIBIR_INFORMACOES != 0 {
			fmt.Printf("Execução %d concluída. Tempo: %f s\n", i+1, elapsed)
		}
	}

	criarOutput(prob, listaTempos)
}

func main() {
	rand.Seed(42)

	problema := criarProblema(INPUT_USADO, ALGORITMO_USADO, QUANTIDADE_EXECUCOES)

	switch problema.AlgoritmoUsado {
	case RADIX_SORT:
		executarAlgoritmo(problema, radix.RadixSort)

	case COUNTING_SORT:
		executarAlgoritmo(problema, counting.CountingSort)

	case INTRO_SORT:
		executarAlgoritmo(problema, introsort.IntroSort)

	case TODOS:
		problema.AlgoritmoUsado = RADIX_SORT
		problema.NomeAlgoritmoUsado = "Radix Sort"
		executarAlgoritmo(problema, radix.RadixSort)

		problema.AlgoritmoUsado = COUNTING_SORT
		problema.NomeAlgoritmoUsado = "Counting Sort"
		executarAlgoritmo(problema, counting.CountingSort)

		problema.AlgoritmoUsado = INTRO_SORT
		problema.NomeAlgoritmoUsado = "Intro Sort"
		executarAlgoritmo(problema, introsort.IntroSort)

	default:
		fmt.Println("Algoritmo não implementado.")
	}

	fmt.Println("Algoritmos finalizados com sucesso.")
}