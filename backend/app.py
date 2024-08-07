from typing import Literal, List, Union
import json
import time
from flask import Flask
from flask_socketio import SocketIO, emit
from openai import OpenAI

client = OpenAI()

app = Flask(__name__)
socketio = SocketIO(app)

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

@app.get('/')
def home():
    return {'msg': 'Hello World!'}

@app.get('/api/causes')
def get_causes():
    return {
        'causes': CAUSES,
    }

@app.get('/api/causes/<string:cause>/concerns')
def get_concerns_for_cause(cause: Literal['airport']):
    return {
        'concerns': ['health', 'noise', 'carbin'],
    }

@app.get('/api/areas/<string:area>/mp')
def get_mp_for_area(area: str):
    return {'mp': 'Beary Bearington'}


@socketio.on('message', namespace="/socket")
def get_letter(raw_data):
    data = json.loads(raw_data)
    print(data)
    full_concerns = ', '.join([CONCERN_KEYS[x] for x in data['concerns']])
    concern_string = f"Your name is {data['name']}. Your MP\'s name is {data['mp']}. You are concerned about {full_concerns}"
    final_prompt = f'{PROMPT}\n{concern_string}'
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": final_prompt},
            {"role": "user", "content": "Write the only the email body to your mp arguing against the expansion"},
        ]
    )
    print('STARTING SESSION')
    print(response)
    emit('token', response.choices[0].message.content, namespace='/socket', broadcast=True)
    print('Closing session')

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
