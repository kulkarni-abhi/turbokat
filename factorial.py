"""
Author: Abhishek Kulkarni

A program to print factorial of a given number (recursion)
"""

def factorial(n):
    if n in (0,1):
        return 1
    elif n < 0:
        raise Exception("No factorial exists for negative numbers")
    else:
        return n*factorial(n-1)

print factorial(5)
