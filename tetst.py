# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 13:48:28 2019

@author: Tim
"""

def a(one, two):
    print("A", one, two)
    
def b(one):
    print("B", one)
    
def test(fun):
    
    for i in range(3):
        if fun==a:
            fun(1, 2)
        else:
            fun("BB")
        
test(a)