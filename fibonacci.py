"""
Author: Abhishek Kulkarni

Program to print Nth number in Fibonacci series

Fibonacci is a series of numbers in which each number is 
a sum of 2 preceding numbers.
"""

def fibonacci(N):
    if N in [1,0]:
        return N
    elif N < 0:
        raise Exception("Incorrect input")
    else:
        return (fibonacci(N-1)+fibonacci(N-2))

print fibonacci(9)
