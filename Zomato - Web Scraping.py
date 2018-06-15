import requests
from bs4 import BeautifulSoup
import pandas

# Setting headers as fake agents.
headers = {'User-Agent': 'Mozilla/5.0 Chrome/67.0.3396.87 Safari/537.36'}
response = requests.get("https://www.zomato.com/bangalore/restaurants",headers=headers)
content = response.content
# Parse the HTML output
soup = BeautifulSoup(content,"html.parser")
# Pick all HTML elements as well as their contents under ID : orig-search-list
top_rest = soup.find_all("div",attrs={"id": "orig-search-list"})

# Separating required data from mentioned HTML page data.
rest_name = top_rest[0].find_all("a", attrs={"class": "result-title"})
rest_add = top_rest[0].find_all("div", attrs={"class": "search-result-address"})
rest_rate = top_rest[0].find_all("div", attrs={"class": "rating-popup"})

# Converting required data into array.
list_rest =[]
for i in range(0, len(rest_name)):
    dataframe ={}
    dataframe["rest_name"] = rest_name[i].text.replace('\n', ' ').replace('  ', '')
    dataframe["rest_address"] = rest_add[i].text.replace('\n', ' ').replace('  ', '')
    dataframe["rest_url"] = rest_name[i]['href']
    dataframe["rest_rating"] = rest_rate[i].text.replace('\n', ' ').replace('  ', '')
    # Requesting link or particular restaurant URL to direct to its own page for reviews.
    rest = requests.get(rest_name[i]['href'] + "/reviews",headers=headers)
    rest_content = rest.content
    rest_soup = BeautifulSoup(rest_content,"html.parser")
    rest_reviews = rest_soup.find_all("div",attrs={"class": "rev-text"})
    # Arranging each different review in different rows based on its particular restaurant.
    for ii in range(0, len(rest_reviews)):
        if ii != 0:
            dataframe ={}
            dataframe["rest_name"] = ''
            dataframe["rest_address"] = ''
            dataframe["rest_url"] = ''
            dataframe["rest_rating"] = ''
            dataframe["rest_review"] = rest_reviews[ii].text.replace('\n', ' ').replace('  ', '').replace('Rated', '')
            list_rest.append(dataframe)
        # Making sure that the restaurant details doesn't get copied every time.    
        else:
            dataframe["rest_review"] = rest_reviews[ii].text.replace('\n', ' ').replace('  ', '')
            list_rest.append(dataframe)
            

# Converting all data into pandas dataframes for quicker processing in the future.
df = pandas.DataFrame(list_rest)

# Saving dataframe as a CSV file.
df.to_csv("zomato_res.csv",index=False)