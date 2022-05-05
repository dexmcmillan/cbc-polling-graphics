from polling import OntarioPolling
from regions_list import regions

leaders = {
        "Liberal Party": "Steven Del Duca",
        "Progressive Conservative Party": "Doug Ford",
        "Green Party": "Mike Schreiner",
        "New Democratic Party": "Andrea Horwath",
        "Other": ""
        }

french_names = {
        "Liberal Party": "Parti libéral",
        "Progressive Conservative Party": "Parti progressiste-conservateur",
        "Green Party": "Parti vert",
        "New Democratic Party": "Nouveau Parti démocratique",
        "Other": "Autres"
        }

for region in regions:

    table = OntarioPolling(language=region["language"]).get_data(
        region=region['region'], data_type="share")

    table.data = table.data.iloc[[-1], :].transpose().reset_index().drop(0)
    table.data.columns = ["Party", "Share"]
    table.data = table.data.sort_values("Share", ascending=False)

    table.data["Leader"] = table.data["Party"].replace(leaders)

    table.data["Image"] = (table.data["Party"].replace({
        "Liberal Party": "![](https://newsinteractives.cbc.ca/elections/poll-tracker/ontario/assets/images/ON/LIB_leader.jpg)",
        "Progressive Conservative Party": "![](https://newsinteractives.cbc.ca/elections/poll-tracker/ontario/assets/images/ON/PC_leader.jpg)",
        "Green Party": "![](https://newsinteractives.cbc.ca/elections/poll-tracker/ontario/assets/images/ON/GRN_leader.jpg)",
        "New Democratic Party": "![](https://newsinteractives.cbc.ca/elections/poll-tracker/ontario/assets/images/ON/NDP_leader.jpg)",
        "Other": ""
    })
    )
    
    if region["language"] == "french":
        table.data["Party"] = table.data["Party"].replace(french_names)
    else:
        title = f"Polling averages in {region['region']}"

    table.data["Text"] = "**" + table.data["Party"] + \
        "**" + "<br>" + table.data["Leader"]

    table.data = table.data[["Image", "Text", "Share"]]

    other = table.data.loc[4, :]
    table.data = table.data.drop(4).append(other)

    table.publish(region['CHART_ID'])
