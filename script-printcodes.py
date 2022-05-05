from datawrapper import Datawrapper
import re
import os
from regions_list import regions

try:
    with open('./auth.txt', 'r') as f:
        DW_AUTH_TOKEN = f.read().strip()    
except:
    DW_AUTH_TOKEN = os.environ['DW_AUTH_TOKEN']
    
headers = {
    "Accept": "*/*",
    "Authorization": f"Bearer {DW_AUTH_TOKEN}"
    }

dw = Datawrapper(access_token=DW_AUTH_TOKEN)

codes = []

for region in regions:

    code = dw.get_iframe_code(region["CHART_ID"], responsive=True)
    title = re.search('(?<=title=\").*(?=\" aria)', code).group(0)
    id = re.search('(?<=id=\"datawrapper-chart-).*(?=\" src)', code).group(0)
    
    link = f"https://www.datawrapper.de/_/{id}/"
    
    string = f"**{title}**<br>**View**: {link}<br>**Embed**: {code}"
    print(string)
    codes.append(string)


with open("embed_codes.md", "w") as text_file:
    text_file.write("<br><br>".join(codes))
    
print(len(codes))