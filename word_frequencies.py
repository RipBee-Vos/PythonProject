import csv


filenames = input().split()


word_counts = {}


for filename in filenames:
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            for word in row:
                if word not in word_counts:
                    word_counts[word] = 1
                else:
                    word_counts[word] += 1


for word in word_counts:
    print(f"{word} {word_counts[word]}")
