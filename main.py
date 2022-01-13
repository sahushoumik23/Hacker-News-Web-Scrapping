from bs4 import BeautifulSoup
from pymongo import MongoClient
from PIL import Image
import requests, urllib,io,os


act_url= "https://news.ycombinator.com/"
weburl = "https://news.ycombinator.com/"
data = requests.get(weburl).text
soup = BeautifulSoup(data,'lxml')
client = MongoClient("mongodb://127.0.0.1:27017")
rel1 = client['scrap']['table1']
rel2 = client['scrap']['table2']

def byte_image(url):
    data = requests.get(url).text
    soup = BeautifulSoup(data,'lxml')
    try:
        img_tags = soup.find_all('img')
        img_url = img_tags[len(img_tags)//2].get('src')
        return requests.get(img_url).content
    except:
        return None


def get_para(url):
    desc = ""
    data = requests.get(url).text
    soup = BeautifulSoup(data,'lxml')
    paras = soup.find_all('p')
    for para in paras:
        s = para.text + '\n\n'
        desc += s
    return desc

def get_votes():
    votes_list = soup.find_all('td',class_="subtext")
    votes = []
    for vote in votes_list:
        if vote.find('span',class_='score') == None:
            votes.append(None)
        else:
            votes.append(vote.find('span',class_='score').text)
    return votes

def get_domain(url):
    return url

def main():
    #########################################list of news ##################################################
    news_list = soup.find_all('tr',class_='athing')
    votes = get_votes()
    ##########################Iterating through the list of news######################
    for i,news in enumerate(news_list):
        print("News:",news.find('a',class_='titlelink').text)
        title = news.find('a',class_='titlelink').text
        print("Votes:",votes[i])
        ############################Modifying the URL#####################
        url = news.find('a',class_='titlelink').get('href')
        if url[0:5] == "item?":
            url = act_url+url
        elif url[0:2] == "./":
            url = get_domain(url)
        print("Web URL for the news:",url)
        ############################Going to the actual news############################
        desc = get_para(url)
        print("Description:",desc)
        imgb = byte_image(url)
        # print("Image in byte format:",imgb)
        print()
        rel1.insert_one({"url":url,"title":title})
        rel2.insert_one({"url":url,"metadata":[{"Description":desc,"Image":imgb,"title":title,"Votes":votes[i]}]})

if __name__ == "__main__":
    main()