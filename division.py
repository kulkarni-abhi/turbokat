"""
Author: Abhishek Kulkarni

Program to divide two numbers without using '/' operator 
and return quotient and reminder
"""

def division(num1, num2):
    if (num1 == 0): 
        return 0
    if (num2 == 0): 
        raise Exception("Division by zero error")
      
    negative = 0
      
    # Handling negative numbers 
    if (num1 < 0): 
        num1 = - num1 
          
        if (num2 < 0): 
            num2 = - num2  
        else: 
            negative = true 
                  
    elif (num2 < 0): 
        num2 = - num2  
        negative = true 
      
    # if num1 is greater than equal to num2 
    # subtract num2 from num1 and increase 
    # quotient by one. 
    quotient = 0
  
    while (num1 >= num2): 
        num1 = num1 - num2  
        quotient += 1
      
    # checking if neg equals to 1 then  
    # making quotient negative  
    if (negative): 
            quotient = - quotient  
    return (quotient , num1) 
  
# Driver program 
num1 = 13; num2 = 2
print(division(num1, num2)) 
