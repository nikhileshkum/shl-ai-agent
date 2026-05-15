OFF_TOPIC_KEYWORDS = [
    "salary",
    "legal",
    "lawsuit",
    "visa",
    "tax",
    "immigration",
    "politics",
    "weather",
    "stock market",
    "bitcoin"
]

PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "system prompt",
    "reveal prompt",
    "bypass"
]

# -----------------------------------
# OFF TOPIC DETECTION
# -----------------------------------

def is_off_topic(text):

    text = text.lower()

    return any(
        keyword in text
        for keyword in OFF_TOPIC_KEYWORDS
    )

# -----------------------------------
# PROMPT INJECTION DETECTION
# -----------------------------------

def is_prompt_injection(text):

    text = text.lower()

    return any(
        pattern in text
        for pattern in PROMPT_INJECTION_PATTERNS
    )