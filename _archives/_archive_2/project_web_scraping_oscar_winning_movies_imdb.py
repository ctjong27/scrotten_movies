
# Based on the work found at
# https://jovian.com/munimadhav/project-web-scraping-oscar-winning-movies-imdb-4ffed


# ### Load the libraries needed for the project

import requests #packages that is used to download the content from web
import urllib # packages that is used to work with URL libraries
import requests #package built to make HTTP requests user friendly
import os # package used for file process
import re # package for regular expression - best to have it dont know if it is required or not
from bs4 import BeautifulSoup #a Python library for pulling data out of HTML and XML files
import pandas as pd # the omnipresent of all python to work with dataframes
requests.__version__ # check the version of the package

### Download the page using requests for 2017 Movies
#https://www.imdb.com/search/title/?title_type=feature,tv_movie&release_date=1900-01-01,2100-12-31&groups=oscar_winner,oscar_nominee&countries=us&sort=year,asc&count=10000
oscar_url = 'https://www.imdb.com/search/title/?release_date=2017&groups=oscar_winner' 
oscar_resp = requests.get(oscar_url) #get the content of the url from the request package.
print(oscar_resp.text[:200]) # look at the snapshot of the content

# ### Parse the html source code using BeautifulSoup4
# In the webpage, there are the following items worth noting
# 
# - total number of titles
# - for each title, total number of votes
# - gross income

oscar_soup = BeautifulSoup(oscar_resp.text, 'html.parser') # with the response text created - parse the html

oscar_containers = oscar_soup.find_all("div",{"class" : "lister-item mode-advanced"}) # get all the containers 
print('Containers is of type: ',type(oscar_containers)) # check the type 
print('Number of movies in the container:',len(oscar_containers)) # number of movies in the container


# ### Extract the information and the data that we are trying to about the movies
# 
# **Before we build through the whole script - lets work thru the attributes we want and how to get those attributes with one movie from the container**
# 
# For the project, goal is to extract the following detail for the movies list:
# - movie_id
# - name 
# - genre 
# - year
# - gross
# - rating
# - certificate (Public rating eg. R PG13)
# - duration 
# - rating_count
# - oscar_wins (no longer app)
# - oscar_nominations (no longer app)
# 
# -----
# 
# For each project, the following member association is desired
# (found from https://www.imdb.com/title/{movie_id}/fullcredits)
# - movie_id
# - member_id
# - association_type
# 
# ### As I am specifically interested in the gender and racial representation on screen, I am focusing my interests in members in the following categories
# - Directing
# - Writing
# - Casted
# - Producing
# - Stars (Found on movies page)
# - Casting & Casting Department
# 
# -----
# 
# For each member, the following information is desired
# - member_id
# - name
# - birth_year
# - gender
# - race
# - first_movie_year
# - last_movie_year
# - total_movie_count
# 


# 
# For the project, goal is to extract the following detail for the movies list:
# - movie_id
# ```
#  - found in <script type="application/ld+json"> - json - url
# ```
# - url
# ```
#  - found in <script type="application/ld+json"> - json - url
# ```
# - name 
# ```
#  - found in <script type="application/ld+json"> - json - name
# ```
# - genre 
# ```
#  - found in <script type="application/ld+json"> - json - genre
# ```
# - year
# ```
#  - found in <script type="application/ld+json"> - json - datePublished
# ```
# - rating_count
# ```
#  - found in <script type="application/ld+json"> - json - aggregateRating - ratingCount
# ```
# - rating_value
# ```
#  - found in <script type="application/ld+json"> - json - aggregateRating - ratingValue
# ```
# - gross (May not be needed)
# - certificate (Public rating eg. R PG13) (May not be needed)
# - duration (May not be needed)
# - oscar_wins (May not be needed, but if needed re-filtering from the search view can get the information)
# - oscar_nominations (May not be needed, but if needed re-filtering from the search view can get the information)


# -----
# -----
# Logic
# 
# Loop through the list of all oscar winning and nominated movies.
# 
# For each movie, iterate through the following
# - Director
# ```
# <h4 name="director" id="director" class="dataHeaderWithBorder">Directed by</h4>
# ```
# - Writer
# ```
# <h4 name="writer" id="writer" class="dataHeaderWithBorder">Writing Credits</h4>
# ```
# - Cast
# ```
# In <table class="cast_list">, between <td colspan="4" class="castlist_label"></td> and <td colspan="4" class="castlist_label">Rest of cast listed alphabetically:</td>
# ```
# - Producing
# ```
# <h4 name="producer" id="producer" class="dataHeaderWithBorder">
# ```
# - Casting & Casting Department
# ```
# <h4 name="casting_director" id="casting_director" class="dataHeaderWithBorder">
# ```
# ```
# <h4 name="casting_department" id="casting_department" class="dataHeaderWithBorder">…</h4>
# ``` 
# 


# 
# For each member, verify whether or not member exists in member datatable. If individual exists, move onto next individual.
# 
# 
# ## SEE IF INFORMATION CAN BE SCRAED FROM JSON AT 
# 
# If individual does not exit, add a new member data entry
# - member_id
# ```
#  - found in <script type="application/ld+json"> - json - url
#  - found after https://www.imdb.com/name/
# ```
# - url
# ```
#  - found in <script type="application/ld+json"> - json - url
# ```
# - name
# ```
#  - found in <script type="application/ld+json"> - json - name
# ```
# - birth_year
# ```
#  - found in <script type="application/ld+json"> - json - birthDate
# ```
# - job title (List)
# ```
#  - found in <script type="application/ld+json"> - json - jobTitle
# ```
# - gender
# ```
#  - based on image found at <script type="application/ld+json"> - json - image, or below
#  <div class="ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-s ipc-poster__poster-image ipc-media__img" style="width:100%">flex
#  ```
# - race
# ```
#  - based on image found at <script type="application/ld+json"> - json - image, or below
#  <div class="ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-s ipc-poster__poster-image ipc-media__img" style="width:100%">flex
#  ```
# 


# Order of the looping logic
# 
# ---
# 
# Start with search result of movie list (expansion into tv shows is tentative) (Starting with oscar nominees but may expand to all movies)
# 
# In the iteration of each movie, store the movie_id data into the 'movies' datatable
# 
# ---
# 
# For each of the 'movies' iteration, enter the website and retrieve the rest of 'movies' datatable column data
# 
# ---
# 
# Once 'movies' datatable is populated, run through the /fullcredits/ site in order to retrieve all associated members
# 
# For each individual listing, populate 'movie_member_associations' table
# - Additional logic needs to handle duplicate member for same role
#  - Actually, this may be as simple as running a data_table search and skipping if already exists
# 
# ---
# 
# For each unique member_id in 'movie_member_association', enter the members' website to scrape and store data

oscar_1 = oscar_containers[0] # get the first movie from the container
print('What is the data type of movie:',type(oscar_1)) # observe the tag of the first movie
print('details of the movie: ', len(oscar_1))

oscar_1.div # div tag or a section or division within HTML
oscar_1.a # a or anchor tag defines the href which is hypertext reference or link for the content on the page
oscar_1.h3 # access h3 content 
oscar_1.h3.a # access he anchor tag and now its getting close to get the movie title
movie_name = oscar_1.h3.a.text # now access just the text part from the tag
movie_name
movie_year = oscar_1.h3.find('span', class_ = 'lister-item-year text-muted unbold').text
movie_year
oscar_1.strong # attribute for rating seems to be pretty easy contained witin *strong* tag

# convert to float as expecting to see some decimal places for rating
movie_rating = float(oscar_1.strong.text) 
movie_rating

# now to get the rest attributes group in p tag with different class
oscar_1.find('span', class_ = 'certificate')
movie_certificate = oscar_1.find('span', class_ = 'certificate').text
movie_certificate

# `Not all movies are rated so lets do a helper function to put a 'Not Rated' where not available`
def get_certificate(oscar):
    # cases where there is no certificate assigned - lets give default as Not Rated
    if oscar.find('span', class_ = 'certificate') is not None:
        cert = oscar.find('span', class_ = 'certificate').text
    else:
        cert = 'Not Rated'
    return cert

get_certificate(oscar_1)

movie_runtime = oscar_1.find('span', class_ = 'runtime').text
movie_genre = oscar_1.find('span', class_ = 'genre').text
movie_genre = movie_genre.strip()

v_g_dtl = oscar_1.findAll('span', attrs = {'name' : 'nv'})
movie_votes = v_g_dtl[0]['data-value']
print(movie_votes)

movie_gross = v_g_dtl[1].text
print(movie_gross)

#get vote count 
oscar_1.findAll('span', attrs = {'name' : 'nv'})[0]['data-value']


# get gross 
oscar_1.findAll('span', attrs = {'name' : 'nv'})[1].text

def get_votes_and_gross(oscar):
    oscar = oscar.find_all('span',{"name":"nv"})
    votes_and_gross_list = []
    for data_value in oscar:
        votes_and_gross_list.append(data_value.text)
    if(len(oscar)==2):
        votes=votes_and_gross_list[0]
        gross = votes_and_gross_list[1]
    else:
        votes=votes_and_gross_list[0]
        gross = None
    
    return votes,gross

get_votes_and_gross(oscar_1)

movie_mscore = oscar_1.find('span', class_ = 'metascore').text
movie_mscore.strip()


def meta_score(oscar):
    # for most of the movies metascore is not available and for those default to 0
    if oscar.find('span', class_ = 'metascore favorable') is not None:
        meta = oscar.find('span', class_ = 'metascore favorable').text
    else:
        meta = '0'
    return int(meta)

meta_score(oscar_1)

# assign the start page as the start_url and see if the function returns the pages
url = 'https://www.imdb.com/search/title/?release_date=2000-01-01,2021-12-31&groups=oscar_winner&sort=year,asc&count=100'

# lets do a helper function to get all the pages for 3 pages
def all_oscar_page(start_url):
    all_urls = [] #list to get all urls
    url = start_url # begin page
    while(url != None):  #Loop around all the required webpages and terminates when last page arive!
        all_urls.append(url) # add to the list
        soup = BeautifulSoup(requests.get(url).text,"html.parser") # parser
        
        # this step is where we get next link - in the screenshot below look at the html inspection on 'Next button'
        # use the class function what makes the page to next
        next_links = soup.find_all(class_='lister-page-next next-page') #Extracts the next page link.
        if (len(next_links) == 0):         # If their is no next page, it returns 0.
            url = None
        else:
            next_page = "https://www.imdb.com" + next_links[0].get('href')
            url = next_page
            print(url)
    return all_urls

all_oscar_page(url) # looks like the function is returning correct links!


import requests #packages that is used to download the content from web
import urllib # packages that is used to work with URL libraries
import requests #package built to make HTTP requests user friendly
import os # package used for file process
import re # package for regular expression - best to have it dont know if it is required or not
from bs4 import BeautifulSoup #a Python library for pulling data out of HTML and XML files
import pandas as pd # the omnipresent of all python to work with dataframes
requests.__version__ # check the version of the package


# ### Finally, write and save the info into CSV files
# 
# **Final helper function to get the movie detail data file by year for user given start and end year**


def get_oscar_movies(start_year, end_year):    
    start_year = str(start_year) # get the begin year
    end_year = str(end_year) # get the end year
    url = get_oscar_url(start_year, end_year) # helper function to build url for start and end year
    oscar_movies = get_oscar_movie_detail(url) # get all the movie detail from helper function
    # give the columns new titles
    oscar_col_list = ['Title','Year','IMDB Rating','Rated','Duration','Genre','Metascore','Votes','Gross USD']
    oscar_df = pd.DataFrame(oscar_movies, columns = oscar_col_list)
    
    # write all the oscar winning movies for the period into one file
    csv_name = 'oscar_movies_'+start_year+'-'+end_year+'.csv'
    print('Oscar movies are also saved in {} file'.format(csv_name))
    
    #create a directory to post the files by year
    os.makedirs('movies_data', exist_ok=True)
    # make the data frame group by year as a dictionary
    oscar_movies_year = {j: oscar_df[oscar_df['Year'] == j] for j in oscar_df['Year'].unique()} 
    #loop thru key, value in dictionary to write the files
    for k, v in oscar_movies_year.items():
        v.to_csv('movies_data\oscar_movies_'+'{}.csv'.format(k), index=None)
    return oscar_df


# **A clean looking URL getter than putting together into one big link**


def get_oscar_url(start_year, end_year):    
    base_url = 'https://www.imdb.com/search/title/?'
    release_date = 'release_date='
    sep = ','
    tail_url = '&groups=oscar_winner&sort=year,asc&count=100'
    oscar_url = base_url + release_date + start_year + sep + end_year + tail_url
    return oscar_url


# **lets do a helper function to get all the pages between start and end year**
# 


def all_oscar_page(start_url):
    all_urls = [] #list to get all urls
    url = start_url # begin page
    while(url != None):  #Loop around all the required webpages and terminates when last page arive!
        all_urls.append(url) # add to the list
        soup = BeautifulSoup(requests.get(url).text,"html.parser") # parser
        
        # this step is where we get next link - in the screenshot below look at the html inspection on 'Next button'
        # use the class function what makes the page to next
        next_links = soup.find_all(class_='lister-page-next next-page') #Extracts the next page link.
        if (len(next_links) == 0):         # If their is no next page, it returns 0.
            url = None
        else:
            next_page = "https://www.imdb.com" + next_links[0].get('href')
            url = next_page
            #print(url)
    return all_urls


# **this is where we go thru each page and also the number of movies in that page**


def get_oscar_movie_detail(url):
    oscar_movies = [] # list of movies of data 
    #url = 'https://www.imdb.com/search/title/?release_date=2000-01-01,2021-12-31&groups=oscar_winner&sort=year,asc&count=100'

    for link in all_oscar_page(url):     #Runs the function for all the pages.
        oscar_soup = BeautifulSoup(requests.get(url).text, 'html.parser') #Extracts out the main html code.
        oscar_containers = oscar_soup.find_all("div",{"class" : "lister-item mode-advanced"}) # get all the containers 
        #print(len(oscar_containers))

        #loop through all the movies in the container to get the attributes
        for oscar in oscar_containers: 
            oscar_movies.append(get_movie_info(oscar))
        return oscar_movies


# **getting the movie info**


def get_movie_info(oscar):
    name = oscar.h3.a.text
    year = oscar.h3.find('span', class_ = 'lister-item-year text-muted unbold')
    movie_year = pd.to_numeric(year.text.replace('(','').replace(')','').replace('I',''))
    rating = float(oscar.strong.text)
    certificate = get_certificate(oscar) 
    duration = oscar.find('span', class_ = 'runtime').text
    genre = oscar.find('span', class_ = 'genre').text.strip()
    metascore = meta_score(oscar)
    votes, gross = votes_and_gross(oscar)
    movie_info = [name, movie_year, rating, certificate, duration, genre, metascore, votes, gross]
    return movie_info


# **helper functions to get certificate, metascore, votes, gross**


def get_certificate(oscar):
    # cases where there is no certificate assigned - lets give default as Not Rated
    if oscar.find('span', class_ = 'certificate') is not None:
        cert = oscar.find('span', class_ = 'certificate').text
    else:
        cert = 'Not Rated'
    return cert


def meta_score(oscar):
    # for most of the movies metascore is not available and for those default to 0
    if oscar.find('span', class_ = 'metascore favorable') is not None:
        meta = oscar.find('span', class_ = 'metascore favorable').text
    else:
        meta = '0'
    return int(meta)


def votes_and_gross(oscar):
    oscar = oscar.find_all('span',{"name":"nv"})
    votes_and_gross_list = []
    for data_value in oscar:
        votes_and_gross_list.append(data_value.text)
    if(len(oscar)==2):
        votes=votes_and_gross_list[0]
        gross = votes_and_gross_list[1]
    else:
        votes=votes_and_gross_list[0]
        gross = None   
    return votes,gross


# **Test the final functions**


oscar_df = get_oscar_movies(2010,2020)


oscar_df[:5]


# As a good neighbor, giving the credit where it is due, I have gained my learning from the following links, my appreciation to all of the folks on the world to provide a great content for others to learn.
# 
# Useful Links:\
# https://www.dataquest.io/blog/web-scraping-python-using-beautiful-soup/ \
# https://www.dataquest.io/blog/web-scraping-beautifulsoup/


# **Finally, commit to Jovian with files**


# # Summary
# - Now that there is a process that I can summarize the data into the files from IMDB, am looking forward to explore these datasets in future data analysis exploration (EDA - exploratory data analysis) to make some interesting observations and hopefully some cool plots. More to follow.
# - This is my first ever web scraping project. I hope my notes, notebook and explanations gives a great confidence to beginners like me on how one can make a good web scraping project with the tools on hand and a bit of effort with python learning. 
# - For Starters, this notebook can be a great help to fork, download or run it directly on the jovian page. There is a ton of help out there for every level of coder, (I for one am grateful for all the help from my community, Jovian team and wealth of resources on the web) hopefully this notebook helps!! 
# - Let's go!


