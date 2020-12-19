# Running async code synchronously

This is an example of how async code can be executed from regular blocking code. There are not so many situations when it's required. However, they still happen. 
As an example: a library providing only async API and at some point of time there's a necessity to block the execution until a particular async operation is completed. 

Example code contains sync executions of simple coroutines as well as an illustration of client and server interactions.

This recipe runs well with Python3.9. Please refer to documentation if higher or lower version of Python is used.