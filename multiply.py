"""
Author: Abhishek Kulkarni

Program to multiply N numbers without using * operator
"""

def multiply(nums=[]):
    if 0 in nums:
        return 0
    for i in range(1,len(nums)):
        sum = 0
        counter = 0
        while counter < nums[i]:
            sum += nums[i-1]
            counter += 1
        nums[i] = sum
    return nums[len(nums)-1]

print multiply([2,3,4,5])
