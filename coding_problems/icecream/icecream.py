csv_dict = {"Vanilla":0, "Chocolate":0, "Strawberry":0, "Mint Chocolate Chip":0, "Cookies and Cream":0, "Chocolate Chip Cookie Dough":0,"Butter Pecan":0, "Rocky Road":0, "Neapolitan":0, "Coffee":0}
json_dict = csv_dict.copy()
txt_dict = csv_dict.copy()
# 1. Read ice cream sales data from three shops - csv ice cream shop, json ice cream shop and txt cvs shop to corresponding dictionaries. Keys of the dictionaries are flavors, and the values should be the number of ice cream being sold.
# 1.1 Read data from csv ice cream shop into the dictionary csv_dict. 
import csv
with open('csvIceCreamShop.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        for flavor in row[1:]:
            if flavor in csv_dict:
                csv_dict[flavor] += 1
print(csv_dict)

# 1.2 Read data from json ice cream shop into the dictionary json_dict. 
import json
with open('online_order.json', 'r') as file:
    data = json.load(file)
    for sale in data['sales']:
        for flavor in sale['flavors']:
            if flavor in json_dict:
                json_dict[flavor] += 1
print(json_dict)

# 1.3 Read data from txt ice cream shop into the dictionary txt_dict. 
with open('customers_comments.txt', 'r') as file:
    for line in file:
        for flavor in txt_dict:
            if flavor in line:
                txt_dict[flavor] += 1

print(txt_dict)

import matplotlib.pyplot as plt

# # Sample dictionaries
dict1 = csv_dict
dict2 = json_dict
dict3 = txt_dict

# Bar width
barWidth = 0.25

# Set position of bars on x axis
r1 = range(len(dict1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

# Make the plot
plt.bar(r1, dict1.values(), width=barWidth, edgecolor='grey', label='Dict1')
plt.bar(r2, dict2.values(), width=barWidth, edgecolor='grey', label='Dict2')
plt.bar(r3, dict3.values(), width=barWidth, edgecolor='grey', label='Dict3')

# Add xticks on the middle of the group bars
plt.xlabel('Keys', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(dict1))], dict1.keys())

# Create legend & Show graphic
plt.legend()
plt.show()
