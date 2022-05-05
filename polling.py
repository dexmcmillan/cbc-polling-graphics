import datetime as dt
from datetime import timedelta
import requests
import pandas as pd
from datawrapper import Datawrapper
import os
import locale

class OntarioPolling:
    
    day = ""
    time = ""
    title = ""
    description = ""
    probabilities = ""
    language = ""
    note = ""
    
    def __init__(self, language="english"):
        today = dt.datetime.today()
        self.language = language
        
        os_name = os.name
        
        if os_name == "posix":
            today = today - dt.timedelta(hours=4)
            
        if language == "english":
            locale.setlocale(locale.LC_ALL, 'en_US')
            self.day = today.strftime('%B %d, %Y')
            self.time = today.strftime('%I:%M') + " " + ".".join(list(today.strftime('%p'))).lower() + "."
            self.note = f"Last updated on {self.day} at {self.time}".replace(" 0", " ")
        elif language == "french":
            locale.setlocale(locale.LC_ALL, 'fr_FR')
            self.day = today.strftime('%d %B %Y')
            self.time = today.strftime('%H') + "h" + today.strftime('%M') + "."
            self.note = f"Mis à jour le {self.day} à {self.time}".replace(" 0", " ")
            
        
        
        blurbs = requests.get("https://canopy.cbc.ca/live/poll-tracker/v5/ON").json()['data']["blurbs"]

        self.title = blurbs[0]["blurb_headline"]
        self.description = blurbs[0]["blurb_text"]
        
    def get_probabilities(self):
        probabilities = requests.get("https://canopy.cbc.ca/live/poll-tracker/v5/ON").json()['data']['supplements']
        
        probabilities = pd.json_normalize(probabilities)
        
        probabilities = probabilities.loc[(probabilities["property"].isin(["Probability of Winning", "Probability of Majority"])) & probabilities["property_meta"].isin(["PC", "LIB"]),:]
        probabilities = probabilities.replace({"LIB": "Liberal Party", "PC": "Progressive Conservative Party", "GRN": "Green Party", "NDP": "New Democratic Party", "OTH": "Other"})

        self.probabilities = probabilities
        
        return self 
        
    def get_data(self, region="Ontario", data_type="seats", poll_type="med"):
        
        # Read in data from the poll tracker API into a pandas dataframe.
        raw = requests.get("https://canopy.cbc.ca/live/poll-tracker/v5/ON").json()['data']["stats"]

        # Reshape the data a little bit to prepare it for the datawrapper.
        parties = raw[0]["rows"]["Ontario"].keys()

        data = []
        for party in parties:
            df = pd.json_normalize(raw, record_path=["rows", region, party, data_type], meta=["datetime"])
            
            df["Party"] = party
            df["Region"] = region
            df["Type"] = ["min", "low", "med", "high", "max"] * int((len(df.index)/5))
            data.append(df)

        data = pd.concat(data)
        data["datetime"] = pd.to_datetime(data["datetime"]).dt.date

        self.data = (data
                  .loc[(data["Type"] == poll_type) & (data["Region"] == region), :]
                  .pivot(index="datetime", columns="Party", values=0)
                  .rename(columns={"LIB": "Liberal Party", "PC": "Progressive Conservative Party", "GRN": "Green Party", "NDP": "New Democratic Party", "OTH": "Other"})
                  .reset_index()
        )
        
        return self
        
    def publish(self, CHART_ID, title=None, description=None, update_text=False):

        if title == None:
            title = self.title
            
        if description == None:
            description = self.description
            
        try:
            with open('./auth.txt', 'r') as f:
                DW_AUTH_TOKEN = f.read().strip()    
        except:
            DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']
            
        headers = {
            "Accept": "*/*",
            "Authorization": f"Bearer {DW_AUTH_TOKEN}"
            }

        check_if_exists = requests.get(f"https://api.datawrapper.de/v3/charts/{CHART_ID}", headers=headers)
        print(check_if_exists)
        
        if check_if_exists.status_code == 404:
            print(f"Sorry! Chart with id {CHART_ID} doesn't exist.")
            raise
            
        metadata_update = {
            "annotate": {
                "notes": self.note
            }
        }

        dw = Datawrapper(access_token=DW_AUTH_TOKEN)
        
        try:
            dw.add_data(chart_id=CHART_ID, data=self.data)
        except:
            print(f"Problem! You may have forgotten to call the get_data() method.")
        
        try:    
            if update_text:
                dw.update_chart(chart_id=CHART_ID, title=title)
                dw.update_description(chart_id=CHART_ID, intro=description)
            else:
                pass
            
            dw.update_metadata(chart_id=CHART_ID, properties=metadata_update)
            dw.publish_chart(chart_id=CHART_ID)
            print(f"Chart updated.")
        except:
            print(f"There was a problem!")
            
        return self