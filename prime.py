"""
Author: Abhishek Kulkarni

Program to check if number is prime or not
"""

def is_prime(num):
    k=0
    for i in range(2,num//2+1):
        if(num%i==0):
            k=k+1
    if(k<=0):
        print("Number is prime")
    else:
        print("Number isn't prime")

is_prime(5)
