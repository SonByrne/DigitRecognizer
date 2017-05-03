import pandas as pd
import random as rand
import math as ma
import sys
import hashlib

# The competition datafiles are in the directory ../input
# Read competition data files:
train = pd.read_csv("train.csv")
test  = pd.read_csv("test.csv")

# Write to the log:
print("Training set has {0[0]} rows and {0[1]} columns".format(train.shape))
print("Test set has {0[0]} rows and {0[1]} columns".format(test.shape))
# Any files you write to the current directory get shown as output

def firstCentroids(digits, numClusters):
	centroids = []
	for count in range(0, numClusters):
		index = int(rand.random() * len(digits))
		centroids.append(digits[index])
	return centroids

#def newCentroids(digits, centroids):
    

def closestCentroid(row, centroids):
	bestsse = sys.maxsize
	closestCentroid = 0
	for index in range(0, len(centroids)):
		sse = 0
		currentCentroid = centroids[index]
		for index2 in range(1, len(row)):
			sse += ma.pow((row[index2] - currentCentroid[index2]), 2)
		if sse < bestsse:
			closestCentroid = index
			bestsse = sse
	return closestCentroid

numClusters = 10

digits = []
correctLabels = []
for row in train.values:
	digits.append(row)
	correctLabels.append(row[0])
    
centroids = firstCentroids(digits, numClusters)
finished = 0
while finished == 0:
	labels = []
	counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for index in range(0, len(digits)):
		closestCent = closestCentroid(digits[index], centroids)
		counts[closestCent] = counts[closestCent] + 1
		labels.append(closestCent)
	countsAvg = sum(counts) / 10
	for index in range(0, len(counts)):
		if counts[index] > (countsAvg / 2) and counts[index] < (countsAvg * 2):
			finished = 1
	if finished == 0:
		#TODO: make into function
		for index in range(0, len(counts)):
			avgs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

			for x in labels:
				avgs[digits[x][0]] = avgs[digits[x][0]] + (sum(digits[x]) - digits[x][0])
			for y in range(0, len(avgs)):
				if counts[y] > 0:
					avgs[y] = avgs[y] / counts[y]

			closestDig = []
			for z in avgs:
				closestDig.append([])

			bestDiff = sys.maxsize
			for digit in digits:
				if ((sum(digit) - digit[0]) - avgs[digit[0]])	< bestDiff:
					bestDiff = (sum(digit) - digit[0]) - avgs[digit[0]]
					closestDig[digit[0]] = digit
		 

table = []
for x in range(0, 10):
	table.append([])
	for y in range(0, 10):
		table[x].append(0)
for index in range(0, len(labels)):
	table[correctLabels[index]][labels[index]] = table[correctLabels[index]][labels[index]] + 1

for x in range(0, 11):
	for y in range(0, 11):
		if x == 0:
			if y == 0:
				print("{:>5}".format(" "), end="")
			else:
				print("{:>5}".format(y-1), end="")
			if x == 11:
				print("")
		else:
			if y == 0:
				print("{:>5}".format(x-1), end="")
			else:
				print("{:>5}".format(table[x-1][y-1]), end="")
			if y == 11:
				print("")
	print("")
print("")
