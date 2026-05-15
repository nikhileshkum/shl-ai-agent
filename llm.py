import os

from google import genai
from dotenv import load_dotenv

from prompts import SYSTEM_PROMPT

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()

# -----------------------------------
# CREATE CLIENT
# -----------------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# -----------------------------------
# GENERATE RESPONSE
# -----------------------------------

def generate_reply(user_query, recommendations):

    # -----------------------------------
    # BUILD RECOMMENDATION TEXT
    # -----------------------------------

    rec_names = [
        rec["name"]
        for rec in recommendations
    ]

    rec_text = ", ".join(rec_names)

    # -----------------------------------
    # PROMPT
    # -----------------------------------

    prompt = f"""
    {SYSTEM_PROMPT}

    USER QUERY:
    {user_query}

    RECOMMENDATIONS:
    {rec_text}

    Generate a concise recruiter-style response.
    """

    # -----------------------------------
    # TRY GEMINI
    # -----------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    # -----------------------------------
    # FALLBACK RESPONSE
    # -----------------------------------

    except Exception:

        if recommendations:

            return (
                f"For your requirements, I recommend "
                f"the following SHL assessments: "
                f"{rec_text}. "
                f"These assessments align with the "
                f"technical skills mentioned in the role."
            )

        return (
            "I could not find suitable SHL "
            "assessments for the given query."
        )