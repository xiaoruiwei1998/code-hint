"""
You are a tiktok dancing influencer, and you want to know the best hashtags 
to post videos to attract maximum views. You have the data for top10 trending 
dancing videos in top10videos.csv. You want to know what is the most used 
hashtag(s) by trending videos, and your task is creating a dictionary to store 
the number of occurrences for each hashtag.
"""

# add an example correct answer of the final state
# add unit test
# make the self-report bin with smaller range above 80










import csv
f = open("top10videos.csv", "r")
reader = csv.reader(f)
data = list(reader)

hashtag_str = ''
ct = 0
for item in data:
    ct += 1
    if ct == 1: continue;
    else: 
        hashtag_str += item[6]

list_of_hashtags = hashtag_str.split(',')

# print(list_of_hashtags)

hashtag_dict = {}
for tag in list_of_hashtags:
    if tag in hashtag_dict:
        hashtag_dict[tag] += 1
    else:
        hashtag_dict[tag] = 1

# print(hashtag_dict)


print(sorted(hashtag_dict.items()))

# for i in sorted (hashtag_dict) : 
#         print ((i, hashtag_dict[i]), end =" ") 
    

f.close()


























# import csv
# import json


# # Reading my_videos.csv
# with open('my_videos.csv', 'r') as f:
#     csv_reader = csv.DictReader(f)
#     my_hashtags = [item['Hashtags'].split(",") for item in csv_reader]
    
# # Flatten the list of my hashtags
# my_hashtags = [item for sublist in my_hashtags for item in sublist]

# # Reading trending_videos.json
# with open('trending_videos.json', 'r') as f:
#     trending_videos = json.load(f)

# # Extracting hashtags from trending videos
# trending_hashtags = [video['Hashtags'] for video in trending_videos]

# # Flatten the list of trending hashtags
# trending_hashtags = [item for sublist in trending_hashtags for item in sublist]

# # Count occurrences of each hashtag
# hashtags_dict = {}
# for hashtag in trending_hashtags:
#     hashtags_dict[hashtag] = hashtags_dict.get(hashtag, 0) + 1

# # Sorting dictionary
# sorted_hashtags_dict = dict(sorted(hashtags_dict.items(), key=lambda x: x[1], reverse=True))

# print(sorted_hashtags_dict)

# # # Visualization
# import matplotlib.pyplot as plt

# fig, ax = plt.subplots()

# names = list(sorted_hashtags_dict.keys())
# values = list(sorted_hashtags_dict.values())

# bar_labels = ['red', 'blue', '_red', 'orange']
# bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

# ax.bar(names, values, label=names)

# ax.set_ylabel('Frequency')
# ax.set_title('TikTok ')
# ax.legend(title='Fruit color')

# plt.show()
