REFINEMENT_WORDS = [
    "actually",
    "instead",
    "also",
    "add",
    "remove",
    "include",
    "exclude"
]

# -----------------------------------
# REFINEMENT DETECTION
# -----------------------------------

def is_refinement(text):

    text = text.lower()

    return any(
        word in text
        for word in REFINEMENT_WORDS
    )