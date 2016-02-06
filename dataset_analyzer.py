#!/usr/bin/python

import json
import us
from collections import defaultdict, Counter
import numpy as np
import matplotlib.pyplot as plt
import os
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import re


def business_data_getter(bus_data_path, category='Restaurants'):
    """
    this method converts the json files provided by Yelp, and returns a dictionary of businesses
    of a given category
    :param bus_data_path: the path to the yelp_academic_dataset_business.json file
    :param category: the category of business
    :return: a dictionary where the key is the business_id and the value is the json object of the business
    """
    bus_dict = defaultdict(dict)
    bus_data_file = open(bus_data_path)
    for line in bus_data_file:
        dump = json.dumps(line)
        data = json.loads(json.loads(dump))
        if len(data['categories']) > 0:
            in_us = us.states.lookup(data['state'])
            if category in data['categories'] and in_us is not None:
                bus_dict[data['business_id']] = data
    return bus_dict


def business_subcate_stats(bus_data_path, category='Restaurants'):
    """
    This method provides the counts of the subcategories of a given category of business
    :param bus_data_path: the path to the yelp_academic_dataset_business.json file
    :param category: the category of business
    :return: a dictionary a tuple of two values: the first one is the count of a subcategory and the second one is
    the count of the reviews for that category
    """
    c = Counter()
    bus_dict = business_data_getter(bus_data_path, category)
    for bus in bus_dict:
        l = bus_dict[bus]['categories']
        for item in l:
            if item != category:
                c[item] += bus_dict[bus]['review_count']
    return c


def plot_n_most_reviews(bus_data_path, category='Restaurants', n=10):
    """
    This method plots a bar chart of the top N subcategories under a given category
    based on total review counts
    :param bus_data_path: the path to the yelp_academic_dataset_business.json file
    :param category: the category of business
    :param n: the number of top subcategories
    :return:
    """
    bus_sub_cate_count = business_subcate_stats(bus_data_path, category)
    categories = []
    reviews = []
    for bus in bus_sub_cate_count.most_common(n):
        # print(bus)
        categories.append(bus[0])
        reviews.append(bus[1])

    categories = tuple(categories)
    reviews = tuple(reviews)
    ind = np.arange(n)
    width = 0.4
    fig, ax = plt.subplots()
    bars = ax.bar(ind, reviews, width, color='b')
    ax.set_ylabel('Reviews')
    ax.set_title('Reviews by Categories')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(categories, ha='center', size='small')

    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2, 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')
    autolabel(bars)
    plt.show()
    return


def output_review(bus_data_path, review_data_path, output_path, category='Restaurants', subcate='Mexican'):
    """
    This method generates reviews text files for a given category of business and its subcategory. In the output path
    there will be five folders, and each represents a star rating. Each review will be created as a separate text file
    and named under its review id.
    :param bus_data_path: the path to the yelp_academic_dataset_business.json file
    :param review_data_path: the path to the yelp_academic_dataset_review.json file
    :param output_path: the path to output the review text files
    :param category: the category of business
    :param subcate: the subcategory of a business
    :return:
    """
    bus_dict = business_data_getter(bus_data_path, category)
    review_file = open(review_data_path)
    for line in review_file:
        dump = json.dumps(line)
        data = json.loads(json.loads(dump))
        bus_id = data['business_id']
        # stopwords_list = stopwords.words('english')
        if bus_id in bus_dict and subcate in bus_dict[bus_id]['categories'] and bus_dict[bus_id]['review_count'] >= 100:
            text = data['text']
            output = open(os.path.join(output_path, str(data['stars']), (data['review_id'] + '.txt')), 'w')
            output.write(text)
            output.close()
    return


def content_word_extractor(input_folder_path, output_file):
    """
    This method extracts content words from all the txt files in a folder and generates a txt file of
    the words with their count.
    :param input_folder_path: the path to the folder that contains all source txt files
    :param output_file: the path and filename of the output file
    :return:
    """
    stopword_list = stopwords.words('english')
    output = open(output_file, 'w')
    files = os.listdir(input_folder_path)
    files = [file for file in files if file.endswith('txt')]
    c = Counter()
    for filename in files:
        file = open(os.path.join(input_folder_path, filename))
        for line in file:
            words = re.sub(r'(\w*)(\W+)(\w*|\W*)', r'\1 \3', line).split()
            for word in words:
                word = word.lower()
                if word not in stopword_list:
                    c[word] += 1
    c = sorted(c.items(), key=lambda pair: pair[1], reverse=True)
    for word in c:
        output.write(word[0] + '\t' + str(word[1]) + '\n')
    return

# plot_n_most_reviews('./yelp_academic_dataset_business.json')
output_review('./yelp_academic_dataset_business.json', './yelp_academic_dataset_review.json', './reviews')
"""
n = 1
while n < 6:
    content_word_extractor('./reviews/'+str(n)+'/', './reviews/'+str(n)+'.txt')
    n += 1
"""
