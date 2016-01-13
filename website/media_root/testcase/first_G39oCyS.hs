doubleMe x = x + x
pyth x y = (x * x) + (y * y)
doublesmall x = if x < 5
                then x + x
                else x
arjoonn = "how are you people"
l1 = [1, 2, 3]
l2 = [4, 5, 6]
l1 ++ l2  -- concatenation
-- Takes long since l1 has to be walked first
0:l1  -- append
'A':"rjoonn"
-- indexing is with !!
"Arjoonn Sharma" !! 1
-- List operations include
-- head, tail(last, init)
-- length, null(isnull?), reverse
-- take(Extract), drop(remove first n), maximum, minimum
-- sum, product, elem(like 'in')
[1..20] -- [1,2,3,4,5..]
[1,3..100] -- [1,3,5,7,9..]
take 10 [3,6..]  -- Table of 3 till 10
take 10 (cycle [1, 2, 3]) -- [1,2,3,1,2,3,1,2,3,1]
take 10 (repeat 5) -- [5,5,5,5,5,5,5,5,5,5] 
replicate 3 10 -- [10, 10, 10]
