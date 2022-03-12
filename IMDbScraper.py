import imdb
from bs4 import BeautifulSoup
import requests


class IMDbScraper:


    def __init__(self, name):
        self.Data = {}
        self.Datas=[]
        self.name=name
        self.imdburl="https://www.imdb.com/"
        self.Searchs = self.search(name)
        # Download page
        if len(self.Searchs)>0:
            self.urls=self.generate_url()
            self.download_page()







    def search(self,name):
        IMDB = imdb.IMDb()
        search=IMDB.search_movie(name)
        return search



    def generate_url(self):
        urls=[]
        i=0
        while len(urls)!=6 and i+1!=len(self.Searchs):
            if self.Searchs[i].data['kind']!='episode':
                urls.append(f"{self.imdburl}title/tt{self.Searchs[i].movieID}")
            i+=1
        return urls




    def download_page(self):

        # method for downloading the  page
        for i in self.urls:
            self.page=requests.get(i).text
            self.scrape_data()
            self.scrape_image()
            self.scrape_trailer_link()
            data = self.Data.copy()
            self.Datas.append({'caption': self.tostring(), 'imageurl': data['imageurl']})

    def scrape_trailer_link(self):
        soup = BeautifulSoup(self.page, "html.parser")
        video = soup.find("a", attrs={"class": "ipc-lockup-overlay Slatestyles__SlateOverlay-sc-1t1hgxj-2 fAkXoJ hero-media__slate-overlay ipc-focusable"})
        if video==None:
            self.Data["videourl"] = None
        else:
            video_url=self.imdburl+video.get('href')
            self.Data["videourl"]=video_url



    def scrape_image(self):
        soup=BeautifulSoup(self.page,"html.parser")
        image=soup.find("a",attrs={"class":"ipc-lockup-overlay ipc-focusable"})
        image_url=self.imdburl+image.get('href')
        self.Data["imageurl"]=image_url


    def scrape_data(self):

        #method for scraping out movie title and description

        soup = BeautifulSoup(self.page, "html.parser")
        movie_title = soup.find("h1", {"data-testid": "hero-title-block__title"})
        movie_productyear=soup.find("span",{"class":"TitleBlockMetaData__ListItemText-sc-12ein40-2 jedhex"})
        movie_director=soup.find("a",{"class":"ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})
        movie_description = soup.find("span", {"data-testid": "plot-xl"})
        movie_rate=soup.find("span",{"class":"AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV"})


        total_ratingamount=soup.find("div",{"class":"AggregateRatingButton__TotalRatingAmount-sc-1ll29m0-3 jkCVKJ"})

        self.Data["title"]=movie_title.text
        self.Data["product year"]=movie_productyear.text
        self.Data["description"]=movie_description.text

        if movie_director!=None:
           self.Data["director"]=movie_director.text
        else:
           self.Data["director"] =None

        if movie_rate!=None:
           self.Data["rate"]=movie_rate.text
        else:
           self.Data["rate"] =None

        if movie_rate != None:
           self.Data["total rating"]=total_ratingamount.text
        else:
            self.Data["rate"] = None

    def ResultOfSearch(self):
        Result = []
        for i in range(0, 6):
            Result.append(f"{i + 1}.{self.Searchs[i].data['title']} : {self.Searchs[i].data['year']}")
        return Result

    def tostring(self):
        directortxt=''
        if self.Data['director']!=None:
            directortxt=f"Director:{self.Data['director']}"

        text= f"{self.Data['title']} : {self.Data['product year']}\n\n{directortxt} \n\n{self.Data['description']}\n\nrate:{self.Data['rate'] if self.Data['rate']!=None else 'with out rate'}-->Amount of Rating:{self.Data['total rating'] if self.Data['total rating']!=None else '' }\n\n"
        if self.Data['videourl']!=None:
            text+=f"trailer link:\n{self.Data['videourl']}"
        return text