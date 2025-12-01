import sys


try:
    a = 1/0
except Exception as e:    
    print(e)    


print(sys.exc_info())