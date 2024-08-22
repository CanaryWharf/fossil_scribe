from typing import Literal, Dict
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


@app.get('/api/causes')
def get_causes():
    refined_actions = [{'key': x['key'], 'name': x['name']} for x in scribe.actions.values()]
    return {
        'causes': refined_actions,
    }

@app.get('/api/causes/{cause}/concerns')
def get_concerns_for_cause(cause: str):
    concerns = scribe.get_concerns(cause)
    refined_concerns = [{'key': x['key'], 'name': x['name'], 'description': x['description']} for x in concerns]
    return {
        'concerns': refined_concerns,
    }

@app.get('/api/areas/<string:area>/mp')
def get_mp_for_area(area: str):
    return {'mp': 'Beary Bearington'}


@app.post('/api/message-gen')
def generate_letter(data: LetterGenRequest) -> Dict[str, str]:
    final_prompt = scribe.get_prompt(data.cause, data.concerns)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a scribe to write emails to mps. Your MP is currently Christopher Kringle. Here is some background about the current cause"},
            {"role": "system", "content": final_prompt},
            {"role": "user", "content": "Write the only the email body to your mp arguing against the expansion"},
        ]
    )
    return {
        'msg': response.choices[0].message.content,
    }

folder = os.path.dirname(__file__)

app.mount("/", StaticFiles(directory=os.path.join(folder, "dist"), html=True), name="static")
