module Introsort.Introsort where

import Data.List (partition)

introSort :: [Int] -> [Int]
introSort xs = introsort xs (2 * floor (logBase 2 (fromIntegral (length xs) :: Double)))

introsort :: [Int] -> Int -> [Int]
introsort xs depth
  | length xs < 16 = insertion xs
  | depth == 0     = heapSort xs
  | otherwise      =
      let (l, r) = partition (<= pivot) rest
      in introsort l (depth - 1) ++ [pivot] ++ introsort r (depth - 1)
  where
    pivot = head xs
    rest  = tail xs

-- insertion sort
insertion :: [Int] -> [Int]
insertion = foldr ins []
  where
    ins x [] = [x]
    ins x (y:ys)
      | x <= y    = x:y:ys
      | otherwise = y : ins x ys

-- heap sort simplificado (didático)
heapSort :: [Int] -> [Int]
heapSort [] = []
heapSort xs =
  let m = maximum xs
  in heapSort (remove m xs) ++ [m]

remove :: Eq a => a -> [a] -> [a]
remove _ [] = []
remove x (y:ys)
  | x == y    = ys
  | otherwise = y : remove x ys

main :: IO ()
main = do
    let lista = [42, 7, 19, 3, 88, 15, 60, 1, 34, 27]
    putStrLn $ "Antes:  " ++ show lista
    putStrLn $ "Depois: " ++ show (introSort lista)