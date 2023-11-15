
# 1. Read ice cream sales data from three shops - csv ice cream shop, json ice cream shop and txt cvs shop to corresponding dictionaries. Keys of the dictionaries are flavors, and the values should be the number of ice cream being sold.
# 1.1 Read data from csv ice cream shop into the dictionary csv_dict. 
import csv

csv_dict = {"Vanilla":0, "Chocolate":0, "Strawberry":0, "Mint Chocolate Chip":0, "Cookies and Cream":0, "Chocolate Chip Cookie Dough":0,"Butter Pecan":0, "Rocky Road":0, "Neapolitan":0, "Coffee":0}
with open('csvIceCreamShop.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        for flavor in row[1:]:
            if flavor in csv_dict:
                csv_dict[flavor] += 1
    
