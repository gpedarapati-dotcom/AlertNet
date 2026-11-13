# AlertNet - AI Flood Emergency Dataset

DATASET = [
    # -------------------------
    # CRITICAL
    # -------------------------
    ("Water entered my house and my family is trapped", "CRITICAL"),
    ("Child is trapped inside the flooded house", "CRITICAL"),
    ("Please rescue us immediately, water is rising fast", "CRITICAL"),
    ("Person is drowning in flood water", "CRITICAL"),
    ("老人 trapped in flood water please rescue", "CRITICAL"),
    ("Need emergency rescue, people are trapped", "CRITICAL"),
    ("My mother is unable to leave the flooded house", "CRITICAL"),
    ("People are trapped on the roof", "CRITICAL"),
    ("House is completely surrounded by flood water", "CRITICAL"),
    ("Someone is injured and needs immediate rescue", "CRITICAL"),
    ("Paani ghar ke andar aa gaya hai, bachao", "CRITICAL"),
    ("Baccha flood mein phas gaya hai, jaldi help chahiye", "CRITICAL"),
    ("Ghar mein log phas gaye hain rescue chahiye", "CRITICAL"),
    ("Paani bahut tezi se badh raha hai bachao", "CRITICAL"),
    ("పిల్లలు వరదలో చిక్కుకున్నారు వెంటనే సహాయం కావాలి", "CRITICAL"),
    ("ఇంట్లోకి వరద నీరు వచ్చింది మమ్మల్ని రక్షించండి", "CRITICAL"),
    ("నీరు చాలా వేగంగా పెరుగుతోంది వెంటనే రక్షించండి", "CRITICAL"),

    # -------------------------
    # URGENT
    # -------------------------
    ("Water level is increasing near my house", "URGENT"),
    ("Road is completely flooded", "URGENT"),
    ("We need help evacuating this area", "URGENT"),
    ("Flood water is entering the street", "URGENT"),
    ("Our vehicle is stuck in flood water", "URGENT"),
    ("Water is getting higher every minute", "URGENT"),
    ("Please send help to our neighborhood", "URGENT"),
    ("The bridge is covered with flood water", "URGENT"),
    ("Many houses are surrounded by water", "URGENT"),
    ("Need evacuation assistance", "URGENT"),
    ("Mere ghar ke paas paani badh raha hai", "URGENT"),
    ("Road pura paani mein doob gaya hai", "URGENT"),
    ("Humein evacuation ke liye help chahiye", "URGENT"),
    ("Gaadi flood water mein phas gayi hai", "URGENT"),
    ("వరద నీరు రోడ్డుపైకి వచ్చింది", "URGENT"),
    ("మా ప్రాంతంలో నీటి మట్టం పెరుగుతోంది", "URGENT"),
    ("ఇక్కడి నుంచి మమ్మల్ని తరలించాలి", "URGENT"),

    # -------------------------
    # INFORMATIONAL
    # -------------------------
    ("There is some waterlogging on the road", "INFORMATIONAL"),
    ("Flood water is visible near the street", "INFORMATIONAL"),
    ("There is water around the neighborhood", "INFORMATIONAL"),
    ("Road has minor flooding", "INFORMATIONAL"),
    ("Waterlogging reported near the market", "INFORMATIONAL"),
    ("Some streets have standing water", "INFORMATIONAL"),
    ("Flood water is present near the bridge", "INFORMATIONAL"),
    ("There is water accumulation outside the house", "INFORMATIONAL"),
    ("Road is wet because of heavy rain", "INFORMATIONAL"),
    ("Small amount of water on the road", "INFORMATIONAL"),
    ("Road par thoda paani jama hai", "INFORMATIONAL"),
    ("Gali mein paani jama hai", "INFORMATIONAL"),
    ("Sadak par paani hai", "INFORMATIONAL"),
    ("Market ke paas waterlogging hai", "INFORMATIONAL"),
    ("రోడ్డుపై కొంత నీరు నిలిచింది", "INFORMATIONAL"),
    ("వీధిలో నీరు ఉంది", "INFORMATIONAL"),
    ("వంతెన దగ్గర వరద నీరు కనిపిస్తోంది", "INFORMATIONAL"),
]


def get_dataset():
    """Return the training dataset."""
    texts = [item[0] for item in DATASET]
    labels = [item[1] for item in DATASET]

    return texts, labels


if __name__ == "__main__":
    texts, labels = get_dataset()

    print("AlertNet AI Dataset")
    print("-------------------")
    print("Total examples:", len(texts))
    print("CRITICAL:", labels.count("CRITICAL"))
    print("URGENT:", labels.count("URGENT"))
    print("INFORMATIONAL:", labels.count("INFORMATIONAL"))