module Counting.Counting where

import qualified Data.Vector.Unboxed         as V
import qualified Data.Vector.Unboxed.Mutable as MV
import Control.Monad (forM_)
import Control.Monad.ST (runST, ST)

countingSort :: [Int] -> [Int]
countingSort listaOriginal = runST $ do

    lista <- V.thaw (V.fromList listaOriginal)   
    
    let tamanho = length listaOriginal
    let maiorValor = maximum listaOriginal
    
    count <- MV.replicate (maiorValor+1) 0
    
    forM_ [0..tamanho-1] $ \i ->do
        posicao <- MV.read lista i
        MV.modify count (+1) posicao
    
    forM_ [1..maiorValor] $ \i ->do
        modificador <- MV.read count (i-1)
        MV.modify count (+modificador) i
        
    aux <- MV.replicate (tamanho) 0
    
    forM_ [tamanho-1,tamanho-2..0] $ \i ->do
        valor <- MV.read lista i
        indice <- MV.read count valor
        MV.write aux (indice-1) valor
        MV.modify count (subtract 1) valor
        
    aux2 <- V.freeze aux
    
    return (V.toList aux2)