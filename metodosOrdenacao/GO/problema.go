package main

import (
	"bufio"
	"fmt"
	"os"
	"time"
)

const (
	ESCOLHER_EM_EXECUCAO = 0
	RADIX_SORT           = 1
	COUNTING_SORT        = 2
	INTRO_SORT           = 3
	TODOS                = 4
)

const (
	INPUT1 = "inputs/input1.dat"
	INPUT2 = "inputs/input2.dat"
	INPUT3 = "inputs/input3.dat"
	INPUT4 = "inputs/input4.dat"
	INPUT5 = "inputs/input5.dat"
	INPUT6 = "inputs/input6.dat"
)

type Problema struct {
	Lista               []int
	Tamanho             int
	NomeInput           string
	AlgoritmoUsado      int
	NomeAlgoritmoUsado string
	QuantidadeExecucoes int
}

func lerInput(prob *Problema, filename string) {
	file, err := os.Open(filename)
	if err != nil {
		fmt.Printf("\033[31mErro ao abrir arquivo: %s\033[0m\n", filename)
		os.Exit(1)
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	// lê tamanho
	var tamanho int
	fmt.Fscan(reader, &tamanho)

	prob.Tamanho = tamanho
	prob.Lista = make([]int, tamanho)

	// leitura direta (MUITO mais rápida)
	fmt.Println("Lendo arquivo...")
	for i := 0; i < tamanho; i++ {
		_, err := fmt.Fscan(reader, &prob.Lista[i])
		if err != nil {
			fmt.Println("Erro ao ler número.")
			os.Exit(1)
		}
		
	}

	fmt.Println("Arquivo lido com sucesso.")
}

func obterNomeInput(input int, nomeInput *string) {
	if input == ESCOLHER_EM_EXECUCAO {
		for {
			fmt.Println("Escolha o Input:")
			fmt.Println("1-6")
			fmt.Print("Resposta: ")

			var escolha int
			fmt.Scan(&escolha)

			if escolha >= 1 && escolha <= 6 {
				input = escolha
				break
			}
			fmt.Println("Opção inválida.")
		}
	}

	switch input {
	case 1:
		*nomeInput = INPUT1
	case 2:
		*nomeInput = INPUT2
	case 3:
		*nomeInput = INPUT3
	case 4:
		*nomeInput = INPUT4
	case 5:
		*nomeInput = INPUT5
	case 6:
		*nomeInput = INPUT6
	}
}

func obterAlgoritmoUsado(algoritmo int, algoritmoUsado *int) {
	if algoritmo == ESCOLHER_EM_EXECUCAO {
		for {
			fmt.Println("1-Radix \n2-Counting \n3-Intro \n4-Todos")
			fmt.Print("Resposta: ")

			var escolha int
			fmt.Scan(&escolha)

			if escolha >= 1 && escolha <= 4 {
				algoritmo = escolha
				break
			}
			fmt.Println("Inválido.")
		}
	}
	*algoritmoUsado = algoritmo
}

func obterQuantidadeExecucoes(q int, out *int) {
	if q == ESCOLHER_EM_EXECUCAO {
		for {
			fmt.Print("Execuções: ")

			var escolha int
			fmt.Scan(&escolha)

			if escolha >= 1 {
				q = escolha
				break
			}
			fmt.Println("Inválido.")
		}
	}
	*out = q
}

func criarProblema(input, algoritmo, quantidade int) *Problema {
	prob := &Problema{}

	obterNomeInput(input, &prob.NomeInput)
	obterAlgoritmoUsado(algoritmo, &prob.AlgoritmoUsado)
	prob.NomeAlgoritmoUsado = map[int]string{
		RADIX_SORT:  "Radix Sort",
		COUNTING_SORT: "Counting Sort",
		INTRO_SORT:  "Intro Sort",
	}[prob.AlgoritmoUsado]
	obterQuantidadeExecucoes(quantidade, &prob.QuantidadeExecucoes)

	lerInput(prob, prob.NomeInput)

	return prob
}

func criarOutput(prob *Problema, tempos []float64) {
	nomeArquivo := fmt.Sprintf("outputs/output_%d.dat", time.Now().Unix())

	file, err := os.Create(nomeArquivo)
	if err != nil {
		fmt.Println("Erro ao criar output.")
		return
	}
	defer file.Close()

	fmt.Fprintf(file, "Linguagem: GO\n")
	fmt.Fprint(file, "Algoritmo: ")
	fmt.Fprint(file, prob.NomeAlgoritmoUsado + "\n")
	fmt.Fprintf(file, "Input: %s\n", prob.NomeInput)

	for i, t := range tempos {
		fmt.Fprintf(file, "Execução %d: %f\n", i+1, t)
	}
}