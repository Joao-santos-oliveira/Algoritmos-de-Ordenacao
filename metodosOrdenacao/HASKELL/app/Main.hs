module Main where

import Data.Time.Clock (getCurrentTime, diffUTCTime)
import Control.DeepSeq (deepseq)
import Data.List (sort)
import Data.IORef (readIORef)

import Problema

import Counting.Counting (countingSort)
import Radix.Radix    (radixSort)
import Introsort.Introsort (introSort)

-- ============================================================
-- Flags de configuração
-- Equivalente aos #define no topo de main.c:
--
--   ALGORITMO_USADO      → Nothing = ESCOLHER_EM_EXECUCAO
--                          Just 1..4 = algoritmo fixo
--   INPUT_USADO          → Nothing = ESCOLHER_EM_EXECUCAO
--                          Just 1..6 = input fixo
--   QUANTIDADE_EXECUCOES → Nothing = ESCOLHER_EM_EXECUCAO
--                          Just n  = valor fixo
--   EXIBIR_INFORMACOES   → True/False
-- ============================================================

algoritmoUsadoConfig     :: Maybe Int
algoritmoUsadoConfig      = Nothing   -- Nothing = ESCOLHER_EM_EXECUCAO

inputUsadoConfig         :: Maybe Int
inputUsadoConfig          = Nothing   -- Nothing = ESCOLHER_EM_EXECUCAO

quantidadeExecoesConfig  :: Maybe Int
quantidadeExecoesConfig   = Nothing   -- Nothing = ESCOLHER_EM_EXECUCAO

exibirInformacoes        :: Bool
exibirInformacoes         = False

-- ============================================================
-- Executar Algoritmo 
-- ============================================================

executarAlgoritmo prob funcAlgoritmo = do
    let qtd = quantidadeExecucoes prob

    tempos <- mapM (executarUma (lista prob) funcAlgoritmo) [1..qtd]

    criarOutput prob tempos

  where
    executarUma listaRef func i = do
        listaPrincipal <- readIORef listaRef   -- lê do IORef a cada iteração

        listaPrincipal `deepseq` return ()

        when exibirInformacoes $
            putStrLn $ "\nExecução " ++ show i ++ " em andamento..."

        inicio    <- getCurrentTime
        let resultado = func listaPrincipal
        resultado `deepseq` return ()
        fim       <- getCurrentTime

        let tempo = realToFrac (diffUTCTime fim inicio) :: Double

        when exibirInformacoes $
            putStrLn $ "Execução " ++ show i ++ " concluída. Tempo gasto: " ++ show tempo ++ " segundos."

        return tempo

    when True  action = action
    when False _      = return ()

-- ============================================================
-- Main 
-- ============================================================

main :: IO ()
main = do
    prob <- criarProblema inputUsadoConfig algoritmoUsadoConfig quantidadeExecoesConfig
    
    case algoritmoUsado prob of

        RadixSort    -> executarAlgoritmo prob radixSort

        CountingSort -> executarAlgoritmo prob countingSort

        IntroSort    -> executarAlgoritmo prob introSort

        Todos -> do
            executarAlgoritmo (prob { algoritmoUsado = RadixSort    }) radixSort
            executarAlgoritmo (prob { algoritmoUsado = CountingSort }) countingSort
            executarAlgoritmo (prob { algoritmoUsado = IntroSort    }) introSort

    putStrLn "Algoritmos finalizados com sucesso..."