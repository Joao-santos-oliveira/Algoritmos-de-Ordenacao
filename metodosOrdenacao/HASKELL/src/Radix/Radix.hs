module Radix.Radix where

import qualified Data.Vector.Unboxed         as V
import qualified Data.Vector.Unboxed.Mutable as MV
import Control.Monad (forM_)
import Control.Monad.ST (runST, ST)



radixSort :: [Int] -> [Int]
radixSort [] = []
radixSort xs = runST $ do

    buf_a <- V.thaw (V.fromList xs)
    buf_b <- MV.new (length xs)

    let maiorValor = maximum xs
    passadas <- radixLSD buf_a buf_b maiorValor 1 0


    resultado <- if odd passadas
                    then V.freeze buf_b
                    else V.freeze buf_a

    return (V.toList resultado)



radixLSD :: MV.MVector s Int -> MV.MVector s Int -> Int -> Int -> Int -> ST s Int
radixLSD buf_a buf_b maiorValor expo passadas
    | expo > maiorValor = return passadas
    | otherwise = do
        countingPass buf_a buf_b expo
        
        radixLSD buf_b buf_a maiorValor (expo * 10) (passadas + 1)



countingPass :: MV.MVector s Int -> MV.MVector s Int -> Int -> ST s ()
countingPass src dst expo = do
    let n = MV.length src

    count <- MV.replicate 10 (0 :: Int)

    forM_ [0..n-1] $ \i -> do
        v <- MV.read src i
        let digito = (v `div` expo) `mod` 10
        MV.modify count (+1) digito

    forM_ [1..9] $ \i -> do
        prev <- MV.read count (i-1)
        MV.modify count (+prev) i

    forM_ [n-1, n-2..0] $ \i -> do
        v <- MV.read src i
        let digito = (v `div` expo) `mod` 10
        pos <- MV.read count digito
        MV.write dst (pos - 1) v
        MV.modify count (subtract 1) digito