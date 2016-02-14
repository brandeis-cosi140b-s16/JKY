# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 10:54:02 2016

@author: Carrie
"""
import os, csv

import menu, shutil

class Reviews(object):
    
    def __init__(self, path):
        self.path=path
        #self.doclist = list(os.walk(path))[0][2]
        self.menu = self.getMenuItems()
        self.doclist = self.getReviewContent()
        

    def getMenuItems(self):
        m = menu.menu("restaurants.json", "menu_items")
        menu_items = set(m.menu_items)
        return menu_items
    
    def getReviewContent(self):
        temp_list = list(os.walk(self.path))[0][2]
        for filename in temp_list:
            filepath = os.path.join(self.path, filename)
            
            f = open(filepath,'r')
            mark = False
            for line in f:
                line_list = line.split()
                for word in line_list:
                    if word in self.menu:
                        mark = True
            if mark == False:
                temp_list.remove(filename)
        return temp_list
    
    def copyReviewFile(self, new_path):      
        
        if not os.path.exists(new_path):
            os.makedirs(new_path)
            
        for filename in self.doclist:
            shutil.copy(os.path.join(self.path,filename), new_path)
            
   
path_list = ['1','2','3','4','5']   
total_number = 0  
for path in path_list:
    r = Reviews(path)
    #print r.doclist
    #docl = r.getReviewConten();#the doclist after removal
    r.copyReviewFile('filter' + path)
    #shutil.copy()
    total_number += len(r.doclist)
    #total_number += r.getReviewContent()
    print total_number
    

    