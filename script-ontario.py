from polling import OntarioPolling

polling = OntarioPolling().get_data().publish("VxY9x")

table = OntarioPolling().get_data(data_type="share")

table.data = table.data.iloc[[-1], :].transpose().reset_index().drop(0)
table.data.columns = ["Party", "Share"]
table.data = table.data.sort_values("Share", ascending=False)

table.data["Leader"] = table.data["Party"].replace({
    "Liberal Party": "Steven Del Duca",
    "Progressive Conservative Party": "Doug Ford",
    "Green Party": "Mike Schreiner",
    "New Democratic Party": "Andrea Horwath",
    "Other": ""})

table.data["Image"] = (table.data["Party"].replace({
    "Liberal Party": "![](https://newsinteractives.cbc.ca/elections/poll-tracker/ontario/assets/images/ON/LIB_leader.jpg)",
    "Progressive Conservative Party": "![](https://newsinteractives.cbc.ca/elections/poll-tracker/ontario/assets/images/ON/PC_leader.jpg)",
    "Green Party": "![](https://newsinteractives.cbc.ca/elections/poll-tracker/ontario/assets/images/ON/GRN_leader.jpg)",
    "New Democratic Party": "![](https://newsinteractives.cbc.ca/elections/poll-tracker/ontario/assets/images/ON/NDP_leader.jpg)",
    "Other": ""
    })
)

table.data["Text"] = "**" + table.data["Party"] + "**" + "<br>" + table.data["Leader"]

table.data = table.data[["Image", "Text", "Share"]]

other = table.data.loc[4, :]
table.data = table.data.drop(4).append(other)

table.publish("T9cnh", description="")