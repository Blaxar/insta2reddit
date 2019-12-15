#!/usr/bin/env python3

import urllib.request
from selenium import webdriver
from os.path import normpath, basename
import praw
from getpass import getpass
import argparse

import config as cfg 

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Post an instagram picture into a subreddit')
    parser.add_argument('post_list', metavar='P', type=str, nargs='+',
                        help='Tuples of Instagram posts to repost on reddit. '
                             'Format is <url 1> <subreddit 1> <title 1> <url 2> <subreddit 2> <title 2> ...')
    args = parser.parse_args()

    if len(args.post_list) % 3 != 0:
        abort("Nonsensical number of tokens in the post list, aborting...")

    post_tuples = [tuple(args.post_list[n:n+3]) for n in range(0, len(args.post_list), 3)]

    # Starting up the webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.binary_location = cfg.selenium_chrome_bin
    driver = webdriver.Chrome(chrome_options=options)

    print("Enter your reddit credentials...")

    try:
        reddit = praw.Reddit(client_id = cfg.praw_client_id,
                             client_secret = cfg.praw_client_secret,
                             user_agent = cfg.praw_user_agent,
                             username = input("Username: "),
                             password = getpass(prompt="Password: "))

    except Exception as error: 
        print('ERROR trying to instanciate reddit client: ', error)
        exit(1)

    for (post_url, subreddit_name, submission_title) in post_tuples:

        pictures = []
    
        try:
            # Fecthing page content and parsing image attributes 
            driver.get(post_url)
            post_name = basename(normpath(post_url))
            img_elements = driver.find_elements_by_css_selector("img[alt^='Image may contain:']");

            # For each relevant img element...
            for idx, img_element in enumerate(img_elements):

                pictures.append([])

                # Get the string encoding the set of images (different resolutions)
                src_set = img_element.get_attribute("srcset")
                print(src_set)

                # Individually save each image from the set
                for token in src_set.split(","):
                    url, res = token.split(" ")
                    file_name = "%s_%i_%s.jpg" % (post_name, idx, res)

                    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                        data = response.read() # a `bytes` object
                        out_file.write(data)
                        pictures[idx].append(file_name)

            print("Submitting %s on r/%s with title '%s'" % (pictures[0][-1], subreddit_name, submission_title))

            subreddit = reddit.subreddit(subreddit_name)
            submission = subreddit.submit_image(submission_title, pictures[0][-1])
            submission.reply("[Source](%s)" % post_url)

        except Exception as e:
            print("Error while fetching picture %s, skipping." % pictures[0][-1], e)

    driver.close()
