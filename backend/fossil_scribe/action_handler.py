import os
from typing import List, Dict, Any, Optional
import yaml
from fossil_scribe.gov import get_mp_from_post_code

BASE_PROMPT = '''
'''

class ActionHandler:
    BASE_PATH = os.path.join(os.path.dirname(__file__), 'action_config')

    @classmethod
    def get_all_actions(cls) -> Dict[str, Any]:
        actions = {}
        for item in os.listdir(cls.BASE_PATH):
            if os.path.isfile(os.path.join(cls.BASE_PATH, item)):
                with open(os.path.join(cls.BASE_PATH, item), encoding="utf-8") as fobj:
                    content = yaml.safe_load(fobj)
                    if content.get('enabled', True):
                        key = content['key']
                        actions[key] = content
        return actions

    def __init__(self):
        self.actions = self.get_all_actions()

    def get_recipients(self, cause: str, post_code: Optional[str] = None) -> List[Dict[str, str]]:
        if 'recipients_lookup' in self.actions[cause]:
            lookup = self.actions[cause]['recipients_lookup']
            if lookup['type'] == 'mp_search':
                assert isinstance(post_code, str)
                return [get_mp_from_post_code(post_code)]
        return self.actions[cause]['recipients']

    def get_concerns(self, cause: str) -> List[Dict[str, str]]:
        return self.actions[cause].get('concerns', [])

    def get_prompt(self, cause: str, concern_keys: List[str]) -> str:
        concerns = [x for x in self.get_concerns(cause) if x['key'] in concern_keys]
        prompts = [x['prompt'] for x in concerns]

        return '\n'.join([BASE_PROMPT, *prompts])
