
import requests

import os

response = requests.post(

    "https://api.featherless.ai/v1/chat/completions",

    headers={

        "Authorization": "Bearer rc_77fb922ab7348d1154155dfadb1d2c76a3a9c576a2348982c667ec3997706ce5",

        "Content-Type": "application/json"

    },

    json={

        "model": "mistralai/Mistral-7B-Instruct-v0.3",

        "messages": [{"role": "user", "content": "say hi"}],

        "max_tokens": 10

    }

)

print(response.status_code)

print(response.json())

