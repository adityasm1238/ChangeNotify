from bs4 import BeautifulSoup
import cloudscraper
import os
from pyexcel_ods3 import get_data
from pyexcel_xlsx import save_data

from app.jobs.base import Job

class VisaDecisionJob(Job):
    JOB_NAME = "visaDecisionPoll"
    def __init__(self, id):
        super().__init__(id, self.JOB_NAME)
    
    def run(self):
        scraper = cloudscraper.create_scraper()  
        webPage = scraper.get("https://www.ireland.ie/en/india/newdelhi/services/visas/processing-times-and-decisions/#Delays").text
        soup = BeautifulSoup(webPage, "html.parser")
        f = soup.find("div", attrs={"id": "Visa decisions"})
        baseUrl  ="https://www.ireland.ie"
        fileUrl = None
        for i in f.find_all("a"):
            if(i.get("href").endswith(".ods")):
                fileUrl = i.get("href")
        
        if fileUrl == None:
            self.logger.error("Unable to find Decision URL")
        else:
            if 'fileUrl' in self.context and self.context['fileUrl'] == fileUrl:
                self.logger.debug("No change detected")
            else:
                staticFolder = os.environ['STATIC_DIRECTORY']
                self.context['fileUrl'] = fileUrl
                fileName = fileUrl.split("/")[-1]
                resp = scraper.get(baseUrl+fileUrl) # making requests to server
                with open(staticFolder+'/'+fileName, "wb") as f: # opening a file handler to create new file 
                    f.write(resp.content) # writing content to file
                save_data(staticFolder+'/'+fileName.split(".")[0]+'.xlsx',get_data("test.ods"))
                self.logger.info("New File detected")
        self.dumpContext()



        
