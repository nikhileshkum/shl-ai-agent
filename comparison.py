COMPARE_WORDS = [
    "difference",
    "compare",
    "vs",
    "versus"
]

# -----------------------------------
# COMPARISON DETECTION
# -----------------------------------

def is_comparison(text):

    text = text.lower()

    return any(
        word in text
        for word in COMPARE_WORDS
    )