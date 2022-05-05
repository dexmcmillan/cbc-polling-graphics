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
        "Liberal Party": "Parti libéral de l'Ontario",
        "Progressive Conservative Party": "Parti progressiste-conservateur de l'Ontario",
        "Green Party": "Parti vert de l'Ontario",
        "New Democratic Party": "Nouveau Parti démocratique de l'Ontario",
        "Other": "Les autres"
        }

french_regions = {
        "Northern Ontario": "Nord de l'Ontario",
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
        note = f"Dernière mise à jour: {table.day} à {table.time}".replace(" 0", " ")
    else:
        title = f"Polling averages in {region['region']}"
        note = f"Last updated on {table.day} at {table.time}".replace(" 0", " ")

    table.data["Text"] = "**" + table.data["Party"] + \
        "**" + "<br>" + table.data["Leader"]

    table.data = table.data[["Image", "Text", "Share"]]

    other = table.data.loc[4, :]
    table.data = table.data.drop(4).append(other)

    table.publish(region['CHART_ID'], note=note)
