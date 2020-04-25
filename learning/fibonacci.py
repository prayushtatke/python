#!/usr/bin/python -tt

def fibb():	
    limit = raw_input('Enter a No. :- ')
    a = 0
    b = 1
    for i in range(int(limit)):
	   c = a + b
	   print c
	   (a, b) = (b, c)
	

def fact():
	num = raw_input ('Enter a No. :- ')
	fact = 1
	for i in range(1,int(num)):
		fact = fact * i
	print fact	

def fullPyramid():
	for i in range(x,0,-1):
		a = i - 1
		b = x - a 
		print ' ' * a,'* ' * b
		

def fullPyramidDigit()
   for i in range (1,x):
      a = x - i
      print ' ' * a,
      for r in range (1,i):
         print r,
      print 
		
		
