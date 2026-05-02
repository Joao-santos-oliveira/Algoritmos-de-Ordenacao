module Main where

import Problema
import Data.Time.Clock (diffUTCTime, getCurrentTime)
import System.Random (randomRIO)

-- Altere para ESCOLHER_EM_EXECUCAO ou para os enums de Algoritmos
algoritmoUsado :: Int
algoritmoUsado = escolherEmExecucao

-- Altere para ESCOLHER_EM_EXECUCAO ou para um numero correspondente ao numero do input
inputUsado :: Int
inputUsado = escolherEmExecucao

-- Altere para ESCOLHER_EM_EXECUCAO ou para um numero correspondente ao numero de execucoes
-- Serve para calcular o tempo médio do algoritmo
quantidadeExecucoes :: Int
quantidadeExecucoes = escolherEmExecucao

-- 0 - Falso, 1 - Verdadeiro
exibirInformacoes :: Int
exibirInformacoes = 0

-- Tipo para função de algoritmo
type AlgoritmoFunc = [Int] -> [Int]

-- Executa um algoritmo
executarAlgoritmo :: Problema -> AlgoritmoFunc -> IO ()
executarAlgoritmo prob funcAlgoritmo = do
    let listaPrincipal = lista prob
    let tamanhoLista = tamanho prob
    listaTempos <- executarComTempo prob funcAlgoritmo (quantidadeExecucoes prob) []
    criarOutput prob listaTempos

-- Executa múltiplas vezes e coleta tempos
executarComTempo :: Problema -> AlgoritmoFunc -> Int -> [Double] -> IO [Double]
executarComTempo prob funcAlgoritmo n tempos
    | n <= 0 = return (reverse tempos)
    | otherwise = do
        let indice = (quantidadeExecucoes prob) - n + 1
        when (exibirInformacoes /= 0) $ putStrLn $ "\nExecução " ++ show indice ++ " em andamento..."
        
        inicio <- getCurrentTime
        let _ = funcAlgoritmo (lista prob)
        fim <- getCurrentTime
        let tempo = realToFrac (diffUTCTime fim inicio) :: Double
        
        when (exibirInformacoes /= 0) $ 
            putStrLn $ "Execução " ++ show indice ++ " concluída. Tempo gasto: " ++ show tempo ++ " segundos."
        
        executarComTempo prob funcAlgoritmo (n - 1) (tempo : tempos)

-- Placeholder functions for sorting algorithms
-- Replace with actual implementations from respective algorithm files
radixSort :: [Int] -> [Int]
radixSort arr = arr  -- Implementação do Radix Sort

countingSort :: [Int] -> [Int]
countingSort arr = arr  -- Implementação do Counting Sort

introSort :: [Int] -> [Int]
introSort arr = arr  -- Implementação do Intro Sort

main :: IO ()
main = do
    problema <- criarProblema inputUsado algoritmoUsado quantidadeExecucoes
    
    case (algoritmoUsado problema) of
        1 -> executarAlgoritmo problema radixSort
        2 -> executarAlgoritmo problema countingSort
        3 -> executarAlgoritmo problema introSort
        4 -> do
            let prob1 = problema { algoritmoUsado = 1 }
            executarAlgoritmo prob1 radixSort
            
            let prob2 = problema { algoritmoUsado = 2 }
            executarAlgoritmo prob2 countingSort
            
            let prob3 = problema { algoritmoUsado = 3 }
            executarAlgoritmo prob3 introSort
        _ -> putStrLn "Algoritmo não implementado."
    
    putStrLn "Algoritmos finalizados com sucesso..."
