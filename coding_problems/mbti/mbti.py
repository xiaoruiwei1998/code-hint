import csv

mbti_dict = {}
with open('student_mbti.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        if row[1] == "F":
            if row[2] not in mbti_dict.keys():
                mbti_dict[row[2]] = 1
            else:
                mbti_dict[row[2]] += 1
                
    print(mbti_dict)