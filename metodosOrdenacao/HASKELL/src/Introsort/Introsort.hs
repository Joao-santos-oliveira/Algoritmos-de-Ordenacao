module Introsort.Introsort where


import qualified Data.Vector.Unboxed         as V
import qualified Data.Vector.Unboxed.Mutable as MV
import Control.Monad (when)
import Control.Monad.ST (runST, ST)
import Data.Bits (shiftR)

introSort :: [Int] -> [Int]
introSort lista = runST $ do
    vetor <- V.thaw (V.fromList lista)

    let tamanho = MV.length vetor

    introsort vetor 0 (tamanho - 1) (2 * log2 tamanho)

    vetorOrdenado <- V.freeze vetor
    return (V.toList vetorOrdenado)

log2 :: Int -> Int
log2 n = calcular n 0
  where
    calcular 0 acumulador = acumulador
    calcular valor acumulador =
        calcular (valor `shiftR` 1) (acumulador + 1)

introsort :: MV.MVector s Int -> Int -> Int -> Int -> ST s ()
introsort vetor inicio fim profundidade
    -- Para pequenos intervalos, usa Insertion Sort
    | fim - inicio + 1 < 16 =
        insertionSort vetor inicio fim

    -- Se atingir profundidade máxima, usa HeapSort
    | profundidade == 0 =
        heapSort vetor inicio fim

    -- Caso padrão: QuickSort
    | otherwise = do
        indicePivo <- partition vetor inicio fim

        introsort vetor inicio (indicePivo - 1) (profundidade - 1)
        introsort vetor (indicePivo + 1) fim (profundidade - 1)

insertionSort :: MV.MVector s Int -> Int -> Int -> ST s ()
insertionSort vetor inicio fim =
    mapM_ inserirElemento [inicio + 1 .. fim]
  where
    inserirElemento indiceAtual = do
        chave <- MV.read vetor indiceAtual
        moverElementos chave (indiceAtual - 1)

    moverElementos chave indice
        | indice < inicio =
            MV.write vetor (indice + 1) chave

        | otherwise = do
            valorAtual <- MV.read vetor indice

            if valorAtual > chave
                then do
                    -- Move o elemento uma posição à direita
                    MV.write vetor (indice + 1) valorAtual
                    moverElementos chave (indice - 1)

                else
                    MV.write vetor (indice + 1) chave

partition :: MV.MVector s Int -> Int -> Int -> ST s Int
partition vetor inicio fim = do
    pivo <- MV.read vetor fim

    let percorrer indiceMenor indiceAtual
            | indiceAtual >= fim = do
                MV.swap vetor (indiceMenor + 1) fim
                return (indiceMenor + 1)

            | otherwise = do
                valorAtual <- MV.read vetor indiceAtual

                if valorAtual <= pivo
                    then do
                        MV.swap vetor (indiceMenor + 1) indiceAtual
                        percorrer (indiceMenor + 1) (indiceAtual + 1)

                    else
                        percorrer indiceMenor (indiceAtual + 1)

    percorrer (inicio - 1) inicio

heapSort :: MV.MVector s Int -> Int -> Int -> ST s ()
heapSort vetor inicio fim = do
    let tamanhoHeap = fim - inicio + 1

    mapM_
        (heapify vetor inicio tamanhoHeap)
        [tamanhoHeap `div` 2 - 1, tamanhoHeap `div` 2 - 2 .. 0]

    -- Remove elementos do heap um por um
    mapM_
        (\indice -> do
            MV.swap vetor inicio (inicio + indice)
            heapify vetor inicio indice 0
        )
        [tamanhoHeap - 1, tamanhoHeap - 2 .. 1]

-- Ajusta a propriedade do heap
heapify :: MV.MVector s Int -> Int -> Int -> Int -> ST s ()
heapify vetor deslocamento tamanhoHeap raiz = do

    let filhoEsquerdo = 2 * raiz + 1
        filhoDireito  = 2 * raiz + 2

    let maiorInicial = raiz

    maiorDepoisEsq <-
        if filhoEsquerdo < tamanhoHeap
            then do
                valorEsq <- MV.read vetor (deslocamento + filhoEsquerdo)
                valorMaior <- MV.read vetor (deslocamento + maiorInicial)

                return (
                    if valorEsq > valorMaior
                        then filhoEsquerdo
                        else maiorInicial
                    )

            else
                return maiorInicial

    maiorFinal <-
        if filhoDireito < tamanhoHeap
            then do
                valorDir <- MV.read vetor (deslocamento + filhoDireito)
                valorMaior <- MV.read vetor (deslocamento + maiorDepoisEsq)

                return (
                    if valorDir > valorMaior
                        then filhoDireito
                        else maiorDepoisEsq
                    )

            else
                return maiorDepoisEsq

    when (maiorFinal /= raiz) $ do
        MV.swap vetor
            (deslocamento + raiz)
            (deslocamento + maiorFinal)

        heapify vetor deslocamento tamanhoHeap maiorFinal