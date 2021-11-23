# Webscraping with BeautifulSoup

## Table of Contents
1. [Project Description](#project-description)
2. [Dependencies](#dependencies)
3. [Set-Up](#set-up)
4. [Additional Thoughts](#additonal-thoughts)

## Project Description
This project contains two webscrapers:
1) Scrapes the website for forms matching user's input & returns results as JSON data in a new JSON file
2) Scrapes the website for forms matching user's input & downloads results as PDFs in a new sub-directory of desired form's name

What is webscraping and when is it done?
 * Webscraping is a program written to extract the data you see when you visit the website manually. 
 * Webscraping is done when an website lacks a dedicated API for pulling the data. 
 * It's important to look at the terms and conditions of the website you are scraping and be ethical in your use.
     * The website being scraped in this project has no robots.txt page.
     * The purpose of this project was purely personal / educational. 

## Dependencies
* Python 3.9.8
* Library: BeautifulSoup
* Library: requests

## Set-Up
1. Clone this repo:
    * `cd <your_desired_directory>`
    * `git clone https://github.com/katalinschmidt/webscraping.git`
2. Set-up the virtual environment:
    * `virtualenv env`
    * `source env/bin/activate`
    * `pip3 install -r requirements.txt`
3. For webscraper 1 / form results as JSON data:
    * `$ python3 scrape_forms.py`
    * Input: as prompted
    * Output: new file '/query_results.json' containing JSON data
4. For webscraper 2 / form results as PDF downloads:
    * `$ python3 scrape_downloads.py`
    * Input: as prompted
    * Output: new subdirectory '/{desired_form_name}' containing PDFs

## Additional Thoughts
There are numerous popular webscraping tools and each tool has its own advantages and disadvantages.

In preparation for this project, I looked into the following webscraping tools:
* BeautifulSoup
    * User-friendly
    * Requires dependencies => difficult to transfer code
    * Inefficient (for scaling / larger projects)
* Selenium
    * Versatile (e.g. automated-testing within the same framework)
    * Works well with Javascript
    * Not user-friendly (i.e. not designed w/webscraping in mind)
* Scrapy
    * Efficient (for scaling / larger projects)
    * Written in Python framework => asynchronous capabilities
    * No dependencies => portable
    * Not user-friendly

Due to my personal time constraints, I decided to use BeautifulSoup for this project.
Selenium and Scrapy are tools that I am still unfamiliar with, but look forward to learning!

There are also many ways I could have designed the input/output of information for this project.
For example, shell commands for redirecting and piping could have been required or, to more closely emulate as REST API,
I could have developed a small Flask web application with 'webscraper 1' in particular as an endpoint.

Another design choice I made was to use logging as my tool for debugging.
Given the nature of the raw HTML being returned by GET requests and then being manipulated with BeautifulSoup,
I needed an easy way to read and assess the large amount of data that was the end result of each of these functions and
felt that exporting that data to a separate log file would be the best way to accomplish that.
Logging is something I had not done before, so I greatly appreciate the practice this project has afforded me with that. 
