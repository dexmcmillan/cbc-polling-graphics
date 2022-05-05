from polling import OntarioPolling

test = OntarioPolling().get_probabilities().probabilities.loc[:, ["property", "property_meta", "value"]]
test["property"] = test["property"].str.replace("Probability of ", "")
test.columns = ["Indicator", "Party", "Chance"]
test["text"] = "Probability of " + test["Party"] + " " + test["Indicator"].str.lower()

test = test[["text", "Party", "Chance"]]

test.to_clipboard()

print(test)