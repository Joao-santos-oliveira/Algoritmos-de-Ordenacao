module Problema where

import qualified Data.ByteString.Char8 as BS
import Data.Maybe (mapMaybe)
import Text.Printf (printf)
import System.IO
import Data.IORef (IORef, newIORef)
import System.Exit (exitFailure)
import Data.Time.Clock.POSIX (getPOSIXTime)
import Control.Exception (catch, IOException)
import Control.Monad (when)

-- ============================================================
-- Flags de configuração
-- ============================================================
exibirBarraProgresso :: Bool
exibirBarraProgresso = False   -- False para desativar

-- ============================================================
-- Data
-- ============================================================

data Algoritmo
    = RadixSort
    | CountingSort
    | IntroSort
    | Todos
    deriving (Show, Eq)

-- ============================================================
-- Macros
-- ============================================================

inputPaths :: [FilePath]
inputPaths =
    [ "inputs/input1.dat"
    , "inputs/input2.dat"
    , "inputs/input3.dat"
    , "inputs/input4.dat"
    , "inputs/input5.dat"
    , "inputs/input6.dat"
    ]

-- ============================================================
-- Data
-- ============================================================

data Problema = Problema
    { lista               :: IORef [Int]
    , tamanho            :: Int
    , nomeInput          :: FilePath
    , algoritmoUsado     :: Algoritmo
    , quantidadeExecucoes :: Int
    }

-- ============================================================
-- Ler Input
-- ============================================================

lerInput :: FilePath -> IO [Int]
lerInput filename =
    (do
        conteudo <- BS.readFile filename

        let linhas = BS.lines conteudo

        -- primeira linha: total de números (para a barra de progresso)
        let total = case linhas of
                        (h:_) -> case BS.readInt (BS.strip h) of
                                    Just (n, _) -> n
                                    Nothing     -> 0
                        []    -> 0

        -- resto das linhas: os números
        let linhasNums = drop 1 linhas
            numLinhas  = length linhasNums

        -- processa linha a linha com progresso
        numeros <- mapM (processarLinha numLinhas total) (zip [1..] linhasNums)

        putStrLn "" -- quebra linha após a barra
        return (concat numeros))

    `catch` (\e -> do
        let _ = e :: IOException
        putStrLn $ "\ESC[31m Erro ao abrir o arquivo."
        putStrLn $ " Arquivo não encontrado ou inacessível: " ++ filename ++ "\ESC[0m"
        exitFailure)

  where
    -- parseia inteiros de uma linha usando ByteString (rápido)
    parseLinha :: BS.ByteString -> [Int]
    parseLinha linha = unfoldr BS.readInt (BS.dropWhile (== ' ') linha)
      where
        unfoldr f b = case f b of
            Nothing     -> []
            Just (a, b') -> a : unfoldr f (BS.dropWhile (\c -> c == ' ' || c == ',') b')

    -- processa uma linha e atualiza a barra
    processarLinha :: Int -> Int -> (Int, BS.ByteString) -> IO [Int]
    processarLinha numLinhas total (i, linha) = do
        let nums = parseLinha linha
        when exibirBarraProgresso $ do
            let pct    = (i * 100) `div` max 1 numLinhas
                barLen = pct `div` 5
                bar    = replicate barLen '█' ++ replicate (20 - barLen) '░'
            printf "\r \ESC[36mLendo\ESC[0m [%s] %3d%% (%d/%d nums)" bar pct i total
            hFlush stdout
        return nums

-- ============================================================
-- Obter Input
-- ============================================================

obterNomeInput :: Maybe Int -> IO FilePath
obterNomeInput (Just n)
    | n >= 1 && n <= 6 = return (inputPaths !! (n - 1))
    | otherwise = do
        putStrLn "\ESC[31m Número de input inválido. Escolha entre 1 e 6.\ESC[0m"
        obterNomeInput Nothing
obterNomeInput Nothing = do
    putStrLn " Escolha o Input a ser usado:"
    putStrLn "1. Input 1\n2. Input 2\n3. Input 3\n4. Input 4\n5. Input 5\n6. Input 6"
    putStr "Resposta: "
    hFlush stdout
    linha <- getLine
    case reads linha of
        [(n, "")] | n >= 1 && n <= 6 -> return (inputPaths !! (n - 1))
        _ -> do
            putStrLn "\n \ESC[31m Opção inválida. Por favor, escolha um número entre 1 e 6.\ESC[0m\n"
            obterNomeInput Nothing

-- ============================================================
-- Obter Algoritmo
-- ============================================================

obterAlgoritmo :: Maybe Int -> IO Algoritmo
obterAlgoritmo (Just n) = case n of
    1 -> return RadixSort
    2 -> return CountingSort
    3 -> return IntroSort
    4 -> return Todos
    _ -> do
        putStrLn "\ESC[31m Opção inválida.\ESC[0m"
        obterAlgoritmo Nothing
obterAlgoritmo Nothing = do
    putStrLn "\n Escolha o algoritmo:"
    putStrLn "1. Radix\n2. Counting\n3. Intro Sort\n4. Todos"
    putStr "Resposta: "
    hFlush stdout
    linha <- getLine
    case reads linha of
        [(n, "")] | n >= 1 && n <= 4 -> obterAlgoritmo (Just n)
        _ -> do
            putStrLn "\n \ESC[31m Opção inválida.\ESC[0m\n"
            obterAlgoritmo Nothing

-- ============================================================
-- Obter Quantidade de Execuções
-- ============================================================

obterQuantidadeExecucoes :: Maybe Int -> IO Int
obterQuantidadeExecucoes (Just n)
    | n >= 1    = return n
    | otherwise = do
        putStrLn "\ESC[31m Quantidade inválida.\ESC[0m"
        obterQuantidadeExecucoes Nothing
obterQuantidadeExecucoes Nothing = do
    putStr "\n Digite a quantidade de execuções (1 ou mais): "
    hFlush stdout
    linha <- getLine
    case reads linha of
        [(n, "")] | n >= 1 -> return n
        _ -> do
            putStrLn "\n \ESC[31m Quantidade inválida.\ESC[0m\n"
            obterQuantidadeExecucoes Nothing

-- ============================================================
-- Criar Problema
-- 'Nothing' em cada campo = ESCOLHER_EM_EXECUCAO
-- ============================================================

criarProblema :: Maybe Int -> Maybe Int -> Maybe Int -> IO Problema
criarProblema inputOpc algOpc execOpc = do
    caminho   <- obterNomeInput inputOpc
    alg       <- obterAlgoritmo algOpc
    execucoes <- obterQuantidadeExecucoes execOpc
    nums      <- lerInput caminho
    listaRef  <- newIORef nums          
    return Problema
        { lista               = listaRef  
        , tamanho             = length nums
        , nomeInput           = caminho
        , algoritmoUsado      = alg
        , quantidadeExecucoes = execucoes
        }

-- ============================================================
-- Criar Output
-- ============================================================

nomeAlgoritmo :: Algoritmo -> String
nomeAlgoritmo RadixSort    = "Radix Sort"
nomeAlgoritmo CountingSort = "Counting Sort"
nomeAlgoritmo IntroSort    = "Intro Sort"
nomeAlgoritmo Todos        = "Todos"

criarOutput :: Problema -> [Double] -> IO ()
criarOutput prob tempos = do 
    ts <- getPOSIXTime
    let timestamp  = show (round ts :: Integer)
        nomeArquivo = "outputs/output" ++ timestamp ++ ".dat"

    writeFile nomeArquivo $ unlines $
        [ "Linguagem: Haskell"
        , "Algoritmo: " ++ nomeAlgoritmo (algoritmoUsado prob)
        , "Input: "     ++ nomeInput prob
        , "Tempos de execução (em segundos):"
        ] ++
        zipWith (\i t -> "Execução " ++ show i ++ ": " ++ show t)
                [1 :: Int ..] tempos

    putStrLn $ "Output salvo em: " ++ nomeArquivo

-- ============================================================
-- Exibir Lista (se necessário)
-- ============================================================

exibirLista :: [Int] -> IO ()
exibirLista xs = putStrLn $ unwords (map show xs)