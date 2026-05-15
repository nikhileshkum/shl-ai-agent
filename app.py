from fastapi import FastAPI
from pydantic import BaseModel

from retrieval import search_assessments

from llm import generate_reply

from conversation import needs_clarification

from refinement import is_refinement

from comparison import is_comparison

from guardrails import (
    is_off_topic,
    is_prompt_injection
)

# -----------------------------------
# FASTAPI APP
# -----------------------------------

app = FastAPI()

# -----------------------------------
# REQUEST SCHEMA
# -----------------------------------

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

# -----------------------------------
# HEALTH ENDPOINT
# -----------------------------------

@app.get("/health")

def health():

    return {
        "status": "ok"
    }

# -----------------------------------
# CHAT ENDPOINT
# -----------------------------------

@app.post("/chat")

def chat(request: ChatRequest):

    # -----------------------------------
    # GET LATEST USER MESSAGE
    # -----------------------------------

    latest_user_message = ""

    for msg in reversed(request.messages):

        if msg.role == "user":

            latest_user_message = msg.content

            break

    # -----------------------------------
    # GUARDRAILS
    # -----------------------------------

    if is_off_topic(latest_user_message):

        return {
            "reply": (
                "I can only help with "
                "SHL assessment recommendations."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    if is_prompt_injection(latest_user_message):

        return {
            "reply": (
                "I can only discuss SHL "
                "assessment recommendations."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------------
    # CLARIFICATION
    # -----------------------------------

    clarification_question = needs_clarification(
        request.messages
    )

    if clarification_question:

        return {
            "reply": clarification_question,
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------------
    # BUILD CONVERSATION CONTEXT
    # -----------------------------------

    user_messages = [
        msg.content
        for msg in request.messages
        if msg.role == "user"
    ]

    query = " ".join(user_messages)

    # -----------------------------------
    # HANDLE REFINEMENT
    # -----------------------------------

    if is_refinement(latest_user_message):

        query += " " + latest_user_message

    # -----------------------------------
    # COMPARISON HANDLING
    # -----------------------------------

    if is_comparison(latest_user_message):

        recommendations = search_assessments(
            latest_user_message,
            top_k=2
        )

        comparison_reply = (
            "These assessments differ in "
            "their focus areas, evaluation "
            "style, and intended hiring use cases."
        )

        return {
            "reply": comparison_reply,
            "recommendations": recommendations,
            "end_of_conversation": False
        }

    # -----------------------------------
    # RETRIEVAL
    # -----------------------------------

    recommendations = search_assessments(
        query,
        top_k=5
    )

    # -----------------------------------
    # GENERATE RESPONSE
    # -----------------------------------

    reply = generate_reply(
        query,
        recommendations
    )

    # -----------------------------------
    # END OF CONVERSATION LOGIC
    # -----------------------------------

    end_of_conversation = False

    completion_words = [
        "final",
        "looks good",
        "lock it",
        "done",
        "confirmed",
        "perfect"
    ]

    if any(
        word in latest_user_message.lower()
        for word in completion_words
    ):
        end_of_conversation = True

    # -----------------------------------
    # FINAL RESPONSE
    # -----------------------------------

    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": end_of_conversation
    }