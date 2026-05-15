CLARIFICATION_PATTERNS = [
    "i need an assessment",
    "recommend an assessment",
    "suggest an assessment",
    "need a test",
    "looking for an assessment"
]

# -----------------------------------
# GET ALL USER TEXT
# -----------------------------------

def get_all_user_text(messages):

    texts = []

    for msg in messages:

        if msg.role == "user":

            texts.append(msg.content)

    return " ".join(texts)

# -----------------------------------
# CLARIFICATION LOGIC
# -----------------------------------

def needs_clarification(messages):

    text = get_all_user_text(messages).lower()

    # -----------------------------------
    # VERY SHORT QUERY
    # -----------------------------------

    if len(text.split()) <= 3:

        return (
            "Could you provide more details "
            "about the role or skills you "
            "want to assess?"
        )

    # -----------------------------------
    # GENERIC PATTERNS
    # -----------------------------------

    for pattern in CLARIFICATION_PATTERNS:

        if pattern in text:

            return (
                "What role, seniority level, "
                "or skills should the "
                "assessment focus on?"
            )

    return None