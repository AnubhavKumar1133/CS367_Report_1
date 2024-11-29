Decision Tree

Age  ----> Entropy is -(5/14log5/14 + 9/14log9/14) = 0.94
    Y 3N 2Y -----> Pn = 3/5 and Py = 2/5 Entropy will be -(Pn log Pn + Py log Py) = 0.97
    M 0N 4Y -----> Pn = 0 and Py = 1 Entropy will be 0
    S 2N 3Y -----> Pn = 2/5 and Py = 3/5 Entropy will be -(Pn log Pn + Py log Py) = 0.97

Salary -----> Entropy is  -(5/14log5/14 + 9/14log9/14) = 0.94
    H 2N 2Y -----> Entropy will be 1
    L 1N 3Y -----> Entropy will be -(1/4log1/4 + 3/4log3/4) = 0.811
    M 2N 4Y -----> Entropy will be -(2/6log 2/6 + 4/6log 4/6) = 0.918

Graduate -----> Entropy will be 0.94
    N 4N 3Y -----> Entropy will be -(4/7log 4/7 + 3/7log3/7) = 
    Y 1N 6Y -----> Entropy will be -(1/6log1/6 + 5/6log5/6) = 

Credit Rating
    A 2N 6Y
    E 3N 3Y

Large set initially by asking questions we are dividing the dataset into small chunks. So we should be asking questions about how do we
compute the homogenity of a subset.

Homogenity is also known as the absence of uncertainity in a subset. Can be measured by entropy. 
Pi = probablity of a particular subset.
Formula of Entropy is -summation(Pilog Pi)
Entropy is highest for uniform distribuition.

Calculate the del E after asking the question where del E is the decrement in the Entropy after asking the question. The question that
gives the largest del E should be considered first.

