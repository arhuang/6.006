#!/usr/bin/python

import string
import sys
import math
    # math.acos(x) is the arccosine of x.
    # math.sqrt(x) is the square root of x.

# global variables needed for fast parsing
# translation table maps upper case to lower case and punctuation to spaces
translation_table = string.maketrans(string.punctuation+string.uppercase[0:26],
                                     " "*len(string.punctuation)+string.lowercase[0:26])

def extract_words(filename):
    """
    Return a list of words from a file
    """
    try:
        f = open(filename, 'r')
        doc = f.read()
        lines = doc.translate(translation_table)
        return lines.split()
    except IOError:
        print "Error opening or reading input file: ",filename
        sys.exit()

def vector_angle(D1, D2):
    numerator = inner_product(D1,D2)
    denominator = math.sqrt(inner_product(D1,D1)*inner_product(D2,D2))
    return math.acos(numerator/denominator)

def inner_product(D1,D2):
    sum = 0.0
    for key in D1: 
        if key in D2:
            sum += D1[key]*D2[key]
    return sum

##############################################
## Part a. Count the frequency of each word ##
##############################################
def doc_dist(word_list1, word_list2):
    """
    Returns a float representing the document distance 
    in radians between two files when given the list of
    words from both files
    """
    D1 = {}
    D2 = {}
    for word in word_list1:
        if word in D1:
            D1[word] = D1[word] + 1
        else:
            D1[word] = 1

    for word in word_list2:
        if word in D2:
            D2[word] = D2[word] + 1
        else:
            D2[word] = 1
                    
    return vector_angle(D1,D2)

##############################################
## Part b. Count the frequency of each pair ##
##############################################
def doc_dist_pairs(word_list1, word_list2):
    """
    Returns a float representing the document distance
    in radians between two files based on unique 
    consecutive pairs of words when given the list of
    words from both files
    """
    D1 = {}
    D2 = {}
    for i in range(len(word_list1)-1):
        key = (word_list1[i],word_list1[i+1])
        if key in D1:
            D1[key] = D1[key] + 1
        else:
            D1[key] = 1

    for i in range(len(word_list2)-1):
        key = (word_list2[i],word_list2[i+1])
        if key in D2:
            D2[key] = D2[key] + 1
        else:
            D2[key] = 1
      
    return vector_angle(D1,D2)

#############################################################
## Part c. Count the frequency of the 50 most common words ##
#############################################################
def doc_dist_50(word_list1, word_list2):
    """
    Returns a float representing the document distance
    in radians between two files based on the 
    50 most common unique words when given the list of
    words from both files
    """
    D1 = {}
    D2 = {}
    for word in word_list1:
        if word in D1:
            D1[word] = D1[word] + 1
        else:
            D1[word] = 1

    for word in word_list2:
        if word in D2:
            D2[word] = D2[word] + 1
        else:
            D2[word] = 1

    freq1 = D1.items()
    freq2 = D2.items()
    freq1.sort(key = lambda x: x[0])
    freq1.sort(key = lambda x: x[1], reverse = True)
    freq2.sort(key = lambda x: x[0])
    freq2.sort(key = lambda x: x[1], reverse = True)
    return vector_angle(dict(freq1[:50]),dict(freq2[:50]))
