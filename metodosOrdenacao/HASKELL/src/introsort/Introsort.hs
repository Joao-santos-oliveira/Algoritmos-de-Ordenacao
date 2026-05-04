module Introsort.Introsort where

import qualified Data.Vector.Unboxed         as V
import qualified Data.Vector.Unboxed.Mutable as MV
import Control.Monad (when)
import Control.Monad.ST (runST, ST)
import Data.Bits (shiftR)


introSort :: [Int] -> [Int]
introSort xs = runST $ do
    v <- V.thaw (V.fromList xs)          
    let n = MV.length v
    introsort v 0 (n - 1) (2 * log2 n)  
    sorted <- V.freeze v                 
    return (V.toList sorted)

log2 :: Int -> Int
log2 n = go n 0
  where
    go 0 acc = acc
    go x acc = go (x `shiftR` 1) (acc + 1)


introsort :: MV.MVector s Int -> Int -> Int -> Int -> ST s ()
introsort v lo hi depth
    | hi - lo + 1 < 16 = insertionSort v lo hi
    | depth == 0        = heapSort v lo hi
    | otherwise         = do
        p <- partition v lo hi
        introsort v lo       (p - 1) (depth - 1)
        introsort v (p + 1)  hi      (depth - 1)


insertionSort :: MV.MVector s Int -> Int -> Int -> ST s ()
insertionSort v lo hi =
    mapM_ insertOne [lo + 1 .. hi]
  where
    insertOne i = do
        key <- MV.read v i
        go key (i - 1)
      where
        go key j
            | j < lo    = MV.write v (j + 1) key
            | otherwise = do
                vj <- MV.read v j
                if vj > key
                    then do
                        MV.write v (j + 1) vj
                        go key (j - 1)
                    else MV.write v (j + 1) key


partition :: MV.MVector s Int -> Int -> Int -> ST s Int
partition v lo hi = do
    pivot <- MV.read v hi
    let go i j
          | j >= hi   = do MV.swap v (i + 1) hi
                           return (i + 1)
          | otherwise = do
              vj <- MV.read v j
              if vj <= pivot
                  then do MV.swap v (i + 1) j
                          go (i + 1) (j + 1)
                  else go i (j + 1)
    go (lo - 1) lo


heapSort :: MV.MVector s Int -> Int -> Int -> ST s ()
heapSort v lo hi = do
    let n = hi - lo + 1
    -- constrói o max-heap
    mapM_ (\i -> heapify v lo n i) [n `div` 2 - 1, n `div` 2 - 2 .. 0]
    -- extrai elementos um a um
    mapM_ (\i -> do
        MV.swap v lo (lo + i)
        heapify v lo i 0
        ) [n - 1, n - 2 .. 1]

heapify :: MV.MVector s Int -> Int -> Int -> Int -> ST s ()
heapify v off n i = do
    let esq = 2 * i + 1
        dir = 2 * i + 2
    maior0 <- return i
    maior1 <- if esq < n
                then do a <- MV.read v (off + esq)
                        b <- MV.read v (off + maior0)
                        return (if a > b then esq else maior0)
                else return maior0
    maior2 <- if dir < n
                then do a <- MV.read v (off + dir)
                        b <- MV.read v (off + maior1)
                        return (if a > b then dir else maior1)
                else return maior1
    when (maior2 /= i) $ do
        MV.swap v (off + i) (off + maior2)
        heapify v off n maior2