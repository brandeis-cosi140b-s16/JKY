# -*- coding: utf-8 -*-
import json, csv, codecs
from pprint import pprint


class menu(object):

    def __init__(self, filename, outfile):
        """initializing a menu"""
        self.data = []
        self.load(filename)
        self.menu_items = self.getItems()
        self.save(outfile)
        #print len(self.menu_items)
		
    def load(self, filename):
        """load the filename in the folder"""
        with open(filename, 'r') as infile:
            for line in infile:
                self.data.append(json.loads(line))

    def getItems(self):
        menu_i = []
        for restaurant in self.data:
            for item in restaurant[u'items']:
                menu_i.append(item[u'name'])
        return sorted(menu_i)
    
    def save(self, outfile):
        file_output = codecs.open(outfile, 'w', 'utf-8')
        for item in self.menu_items:
            file_output.write(item)
            file_output.write('\n')
        file_output.close()




#m = menu("restaurants.json", "menu_items")


"""
for restaurant in m.data:
    for item in restaurant[u'items']:
        menu_items.append(item[u'name'])
menu_i = set(menu_items)
print len(menu_i)"""
