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
            result=self.scrape_data()
            if result==1:
                self.scrape_image()
                self.scrape_trailer_link()
                data = self.Data.copy()
                self.Datas.append({'caption': self.tostring(), 'imageurl': data['imageurl'],'title':data['title'],'product year':data['product year']})

    def scrape_trailer_link(self):
        soup = BeautifulSoup(self.page, "html.parser")
        video = soup.find("a", attrs={"class": "ipc-lockup-overlay sc-5ea2f380-2 gdvnDB hero-media__slate-overlay ipc-focusable"})
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
        movie_description = soup.find("span", {"data-testid": "plot-xs_to_m"})
        movie_title = soup.find("h1", {"data-testid": "hero-title-block__title"})
        movie_director=soup.find("a",{"class":"ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})
        movie_rate=soup.find("span",{"class":"sc-7ab21ed2-1 jGRxWM"})
        total_ratingamount=soup.find("div",{"class":"sc-7ab21ed2-3 dPVcnq"})
        movie_productyear=soup.find("span",{"class":"sc-52284603-2 iTRONr"})





        try:
            self.Data["title"]=movie_title.text
            self.Data["product year"]=movie_productyear.text
            self.Data["description"]=movie_description.text
            self.Data["director"]=movie_director.text
            self.Data["rate"]=movie_rate.text
            self.Data["total rating"]=total_ratingamount.text
            return 1
        except:
            return 0

    def ResultOfSearch(self):
        Result = []
        j = 1
        for i in self.Datas:
            Result.append(f"{j}.{i['title']} : {i['product year']}")
            j += 1
        return Result

    def tostring(self):

        text= f"{self.Data['title']} : {self.Data['product year']}\n\nDirector:\n{self.Data['director']} \n\n{self.Data['description']}\n\nrate:{self.Data['rate']}-->Amount of Rating:{self.Data['total rating']}\n\n"
        if self.Data['videourl']!=None:
            text+=f"trailer link:\n{self.Data['videourl']}"
        return text
