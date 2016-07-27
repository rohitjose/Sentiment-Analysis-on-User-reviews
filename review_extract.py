#!/usr/bin/env python
__author__= 'Rohit Jose'
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Rohit Jose"
__email__ = "rohitjose@gmail.com"
__status__ = "Development"

ROOT_URL = 'http://www.flipkart.com'
PRODUCT_CATEGORY_URL = '/mobiles'

import requests
from lxml import html

URL = 'http://www.flipkart.com/%s/product-reviews/%s?pid=%s&reviewers=all&type=all&sort=most_helpful&start=%s'

def get_page_tree(url):
	''' Returns the page source content of the input URL
		as a parsed XML tree'''
	response = requests.get(url)
	tree = html.fromstring(response.content)
	return tree

def save_user_reviews(file_name,URL):
	'''Saves the review comments to a csv file'''
	
	# Builds the starting page URL for the review comments
	PAGE_URL = URL % '0' 
	# Parse the page source into a tree representation
	tree = get_page_tree(PAGE_URL) 

	# Extract the total number of reviews for the product
	review_total = tree.xpath('//span[@class="fk-font-normal unboldtext"]/text()')[0][1:-1]
	# Calculate the total number of page iterations
	review_iterations = int(int(review_total)/10)
	# Initialize the current page counter for the loop
	current_page_count = 0

	print(review_total)
	f = open(file_name,'w')

	while(current_page_count<review_iterations):
		# Extract the reviews list section in the page
		review_list = tree.xpath('//div[@class="review-list"]')[0]

		# Extract the review rating given by the user
		review_rating = review_list.xpath('//div[@class="fk-stars"]/@title')
		# Extract the date when the review was given
		review_dates = review_list.xpath('//div[@class="date line fk-font-small"]/text()')
		# Extract the title given for the review by the user
		review_titles = review_list.xpath('//div[@class="line fk-font-normal bmargin5 dark-gray"]/strong/text()')
		# Extract the review text content
		review_text = review_list.xpath('//span[@class="review-text"]/text()')

		for i in range(10):
			# Build the file entry for each user review
			out_string = "%s|%s|%s|%s" % (review_dates[i],review_rating[i][0],review_titles[i],review_text[i])
			out_string = out_string.replace('\n','')
			out_string = out_string.replace('\t','')
			# Write the user review into the cev file
			f.write(out_string)
			f.write('\n')

		# Increment the page count value by 10
		current_page_count += 1
		print(current_page_count)
		# Reform the page URL to get the next 10 user reviews
		PAGE_URL = URL % str(current_page_count*10)
		# Parse the page source to the tree representation
		tree = get_page_tree(PAGE_URL) 


	f.close()

# print(review_total,review_iterations)

save_user_reviews('customer_reviews.txt',URL)


