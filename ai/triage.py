import os
import re
import joblib


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "model.joblib"
)

model = joblib.load(MODEL_PATH)


# ============================================================
# CRITICAL EMERGENCY KEYWORDS
# ============================================================

CRITICAL_KEYWORDS = [

    # English
    "trapped",
    "stranded",
    "drowning",
    "life threatening",
    "life-threatening",
    "rooftop",
    "rescue",
    "children trapped",
    "child trapped",
    "people trapped",
    "person trapped",
    "rapidly rising water",
    "can't escape",
    "cannot escape",
    "unable to leave",
    "injured",

    # Hindi / Hinglish
    "bachao",
    "phans gaya",
    "phans gaye",
    "rescue chahiye",
    "jaldi help chahiye",
    "madad chahiye",

    # Telugu
    "చిక్కుకున్నారు",
    "చిక్కుకున్నాడు",
    "చిక్కుకుంది",
    "రక్షించండి",
    "వెంటనే సహాయం కావాలి",
    "వెంటనే రక్షించండి",
]


# ============================================================
# NEGATION WORDS
# ============================================================

NEGATION_PHRASES = [
    "no one is",
    "no one was",
    "nobody is",
    "nobody was",
    "not",
    "no",
    "without",
    "never",
    "isn't",
    "is not",
    "wasn't",
    "was not",
    "aren't",
    "are not",
    "don't",
    "do not",
]


# ============================================================
# AI TRIAGE
# ============================================================

def classify_sos(description):
    """
    Classify an SOS report as CRITICAL,
    URGENT, or INFORMATIONAL.
    """

    text = description.strip()
    text_lower = text.lower()

    # --------------------------------------------------------
    # CHECK CRITICAL KEYWORDS
    # --------------------------------------------------------

    detected_keywords = []

    for keyword in CRITICAL_KEYWORDS:

        if keyword not in text_lower:
            continue

        # Check whether keyword is being used negatively
        is_negated = False

        for negation in NEGATION_PHRASES:

            pattern = (
                rf"\b{re.escape(negation)}\b"
                rf".{{0,35}}"
                rf"\b{re.escape(keyword)}\b"
            )

            if re.search(pattern, text_lower):
                is_negated = True
                break

        if not is_negated:
            detected_keywords.append(keyword)

    # --------------------------------------------------------
    # CRITICAL OVERRIDE
    # --------------------------------------------------------

    if detected_keywords:

        return {
            "severity": "CRITICAL",
            "score": 1.0,
            "explanation": (
                "Safety escalation triggered by emergency terms: "
                + ", ".join(detected_keywords)
            )
        }

    # --------------------------------------------------------
    # ML MODEL CLASSIFICATION
    # --------------------------------------------------------

    probabilities = model.predict_proba([text])[0]
    classes = model.classes_

    best_index = probabilities.argmax()

    severity = classes[best_index]
    score = float(probabilities[best_index])

    return {
        "severity": severity,
        "score": round(score, 2),
        "explanation": (
            f"ML model classified the report as {severity} "
            f"based on the SOS text."
        )
    }


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    test_messages = [

        # Should be CRITICAL
        "Water entered my house and my children are trapped on the rooftop",

        # Should normally be URGENT or INFORMATIONAL
        "Road is heavily flooded and vehicles cannot pass",

        # Should be INFORMATIONAL
        "There is minor waterlogging near the road",

        # Should be CRITICAL because of Telugu emergency phrase
        "ఇంట్లోకి నీరు వచ్చింది, వెంటనే సహాయం కావాలి",

        # Should NOT become CRITICAL because trapped/injured are negated
        "There is minor waterlogging. No one is trapped or injured."
    ]

    print("\nAlertNet AI Triage Test")
    print("======================")

    for message in test_messages:

        result = classify_sos(message)

        print("\nSOS:", message)
        print("Severity:", result["severity"])
        print("Model score:", result["score"])
        print("Explanation:", result["explanation"])