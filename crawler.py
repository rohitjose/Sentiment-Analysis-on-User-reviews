#!/usr/bin/env python
__author__= 'Rohit Jose'
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Rohit Jose"
__email__ = "rohitjose@gmail.com"
__status__ = "Development"

import requests
from lxml import html

ROOT_URL = 'http://www.flipkart.com'
PRODUCT_CATEGORY_URL = '/mobiles/~mobileexclusives/pr?sid=tyy%2C4io&otracker=ch_vn_mobile_main_Best%20Sellers_View_All'

def get_page_tree(url):
	''' Returns the page source content of the input URL
		as a parsed XML tree'''
	response = requests.get(url)
	tree = html.fromstring(response.content)
	return tree

def get_product_params(link):
	''' Returns the product information based on the URL
		value that is passed as the parameter value'''
	data = link.split('/')
	product = {}
	product['name'] = data[1]
	product['itemno'],product['pid'] = data[3].split('?')
	product['pid'] = product['pid'][4:]
	return product

def get_review_url(product):
	PRODUCT_URL = ROOT_URL + '/%s/product-reviews/%s?pid=%s&reviewers=all&type=all&sort=most_helpful&start=' % \
	(product['name'],product['itemno'],product['pid'])
	return PRODUCT_URL

def save_user_reviews(file_name,URL,product_name):
	'''Saves the review comments to a csv file'''
	
	# Builds the starting page URL for the review comments
	PAGE_URL = URL + '0' 
	# Parse the page source into a tree representation
	tree = get_page_tree(PAGE_URL) 

	# Extract the total number of reviews for the product
	review_total = tree.xpath('//span[@class="fk-font-normal unboldtext"]/text()')[0][1:-1]
	# Calculate the total number of page iterations
	review_iterations = int(int(review_total)/10)
	# Initialize the current page counter for the loop
	current_page_count = 0

	print(review_total)
	f = open(file_name,'a')

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
			out_string = "%s|%s|%s|%s|%s" % (product_name,review_dates[i],review_rating[i][0],review_titles[i],review_text[i])
			out_string = out_string.replace('\n','')
			out_string = out_string.replace('\t','')
			# Write the user review into the cev file
			f.write(out_string)
			f.write('\n')

		# Increment the page count value by 10
		current_page_count += 1
		print(current_page_count)
		# Reform the page URL to get the next 10 user reviews
		PAGE_URL = URL + str(current_page_count*10)
		# Parse the page source to the tree representation
		tree = get_page_tree(PAGE_URL) 


	f.close()

if __name__ == '__main__':
	# Parse the product page to identify the individual product links
	tree = get_page_tree(ROOT_URL + PRODUCT_CATEGORY_URL)
	# Extract the URL links for each product in the main page based on the 
	# specific anchor <a> tag
	product_links = tree.xpath('//a[@data-tracking-id="prd_img"]/@href')

	# Build the product information list out of the URL assosication
	product_information_list = []
	for link in product_links:
		#product_information_list.append(get_product_params(link))
		product = get_product_params(link)
		URL = get_review_url(product)
		save_user_reviews('customer_reviews.txt',URL,product['name'])



	