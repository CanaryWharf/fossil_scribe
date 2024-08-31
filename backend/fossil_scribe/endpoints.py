from typing import Literal, Dict, Optional
import os
import yaml
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from fossil_scribe.models import LetterGenRequest
from fossil_scribe.action_handler import ActionHandler

app = FastAPI()
client = OpenAI()

scribe = ActionHandler()


@app.get("/api/causes")
def get_causes():
    refined_actions = [
        {
            "key": x["key"],
            "name": x["name"],
            "description": x.get("description"),
            "recipients_lookup": x.get("recipients_lookup"),
            "recipients": x.get("recipients"),
        }
        for x in scribe.actions.values()
    ]
    return {
        "causes": refined_actions,
    }


@app.get("/api/causes/{cause}/concerns")
def get_concerns_for_cause(cause: str):
    concerns = scribe.get_concerns(cause)
    refined_concerns = [{"key": x["key"], "name": x["name"], "description": x["description"]} for x in concerns]
    return {
        "concerns": refined_concerns,
    }


@app.get("/api/causes/{cause}/recipients")
def get_recipients_for_cause(cause: str, post_code: Optional[str] = None):
    return {"recipients": scribe.get_recipients(cause, post_code=post_code)}


def _get_email(recipients_string: str, final_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are a scribe to write emails. Your recipients are {recipients_string}. Address them by their full name. You Here is some background about the current cause",
            },
            {"role": "system", "content": final_prompt},
            {
                "role": "user",
                "content": "Write the only subject above 3 dashes (---), then write only the email body regarding your concerns. Don't sign off with yours sincerely or anything similar. Write just the body and subject seperated by dashes. Do not write Subject when stating the subject. If you do not follow the subject with 3 dashes and then the body format, I will be upset.",
            },
        ],
    )
    return response.choices[0].message.content


@app.post("/api/message-gen")
def generate_letter(data: LetterGenRequest) -> dict:
    final_prompt = scribe.get_prompt(data.cause, data.concerns)
    recipients_string = ", ".join([x["name"] for x in scribe.get_recipients(data.cause, post_code=data.postcode)])
    msg = _get_email(recipients_string, final_prompt)
    print(msg)
    subject, email = msg.split("---")
    subject = subject.replace("Subject: ", "")

    return {
        "msg": email.strip(),
        "subject": subject.strip(),
        "recipients": scribe.get_recipients(data.cause, data.postcode),
    }


folder = os.path.dirname(__file__)

app.mount("/", StaticFiles(directory=os.path.join(folder, "dist"), html=True), name="static")
