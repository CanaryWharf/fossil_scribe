from typing import Literal, Dict
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from fossil_scribe.models import LetterGenRequest

app = FastAPI()
client = OpenAI()


PROMPT = '''
You are a local resident of Newham, London. There is a planned airport expansion of City Airport. You don't consider yourself as too fancy. You write all responses in markdown.
'''

CONCERN_KEYS = {
    'health': 'Health issues',
    'noise': 'Noise Pollution',
    'carbon': 'Carbon Emissions',
}
CAUSES = [
    {'name': 'airport', 'title': 'City Airport Expansion'},
]

CONCERNS = [
    {'key': 'health', 'name': 'Health issues with fumes'},
    {'key': 'noise', 'name': 'Noise Pollution'},
    {'key': 'carbon', 'name': 'Carbon released'},
]


@app.get('/api/causes')
def get_causes():
    return {
        'causes': CAUSES,
    }

@app.get('/api/causes/{cause}/concerns')
def get_concerns_for_cause(cause: Literal['airport']):
    return {
        'concerns': CONCERNS,
    }

@app.get('/api/areas/<string:area>/mp')
def get_mp_for_area(area: str):
    return {'mp': 'Beary Bearington'}


@app.post('/api/message-gen')
def generate_letter(data: LetterGenRequest) -> Dict[str, str]:
    full_concerns = ', '.join([CONCERN_KEYS[x] for x in data.concerns])
    concern_string = f"Your name is {data.name}. Your MP\'s name is {data.mp}. You are concerned about {full_concerns}"
    final_prompt = f'{PROMPT}\n{concern_string}'
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": final_prompt},
            {"role": "user", "content": "Write the only the email body to your mp arguing against the expansion"},
        ]
    )
    return {
        'msg': response.choices[0].message.content,
    }

folder = os.path.dirname(__file__)

app.mount("/", StaticFiles(directory=os.path.join(folder, "dist"), html=True), name="static")
