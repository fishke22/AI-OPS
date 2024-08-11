"""
Interfaces the AI Agent to the LLM Provider, model availability depends on
implemented prompts, to use a new model the relative prompts should be written.
"""
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import requests.exceptions
from requests import Session
from ollama import Client, ResponseError
from httpx import ConnectError

from src.agent.memory.base import Role


AVAILABLE_MODELS = {
    'llama3': {
        'options': {
            'temperature': 0.5,
            'num_ctx': 8192
        },
        'tools': True
    },
    'gemma:7b': {
        'options': {
            'temperature': 0.5,
            'num_ctx': 8192
        },
        'tools': False
    },
    'gemma2:9b': {
        'options': {
            'temperature': 0.5,
            'num_ctx': 8192
        },
        'tools': False
    },
    'mistral': {
        'options': {
            'temperature': 0.5,
            'num_ctx': 8192
        },
        'tools': True
    },
}


@dataclass
class Provider(ABC):
    """Represents a LLM Provider"""
    model: str
    client_url: str = 'http://localhost:11434'
    api_key: str | None = None

    @abstractmethod
    def query(self, messages: list):
        """Implement to makes query to the LLM provider"""

    @abstractmethod
    def tool_query(self, messages: list, tools: list | None = None):
        """Implement for LLM tool calling"""


class ProviderError(Exception):
    """Just a wrapper to Exception for error handling
    when an error is caused by the LLM provider"""


@dataclass
class Ollama(Provider):
    """Ollama Interface"""
    client: Client | None = field(init=False, default=None)

    def __post_init__(self):
        if self.model not in AVAILABLE_MODELS.keys():
            raise ValueError(f'Model {self.model} is not available')
        try:
            self.client = Client(host=self.client_url)
        except Exception as err:
            raise RuntimeError(f'Something went wrong: {err}')

    def query(self, messages: list):
        """Generator that returns response chunks."""
        # check types
        message_types_dict = [isinstance(msg, dict) for msg in messages]
        if not isinstance(messages, list) or \
                len(messages) == 0 or \
                False in message_types_dict:
            raise TypeError(f'messages must be a list of dictionaries, found: \n {messages}')

        # check format
        valid_roles = [str(role) for role in [Role.SYS, Role.USER, Role.ASSISTANT]]
        err_message = f'messages must follow the format {{"role": "{valid_roles}", "content": "..."}}'

        # check format - keys
        message_keys = [list(msg.keys()) for msg in messages]
        valid_keys = ['role' in keys and 'content' and len(keys) == 2 in keys for keys in message_keys]
        if False in valid_keys:
            raise ValueError(err_message)

        # check format = values
        message_roles = [msg['role'] in valid_roles for msg in messages]
        message_content = [len(msg['content']) != 0 for msg in messages]
        if False in message_roles or False in message_content:
            raise ValueError(err_message)

        try:
            stream = self.client.chat(
                model=self.model,
                messages=messages,
                stream=True,
                options=AVAILABLE_MODELS[self.model]['options']
            )
            for chunk in stream:
                yield chunk['message']['content']
        except ResponseError as err:
            raise ProviderError(err)

    def tool_query(self, messages: list, tools: list | None = None):
        """"""
        if not AVAILABLE_MODELS[self.model]['tools']:
            raise NotImplementedError(f'Model {self.model} do not implement tool calling')

        if not tools:
            # TODO: should add validation for tools
            raise ValueError('Empty tool list')

        return self.client.chat(
            model=self.model,
            messages=messages,
            tools=tools
        )


@dataclass
class OpenRouter(Provider):
    """OpenRouter Interface"""
    session: Session | None = None

    def __post_init__(self):
        self.session = Session()
        self.models = {
            'gemma:7b': 'google/gemma-2-9b-it:free',
            'mistral': 'mistralai/mistral-7b-instruct:free'
        }

    def query(self, messages: list):
        """Generator that returns response chunks."""
        response = self.session.post(
            url=self.client_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": 'https://github.com/antoninoLorenzo/AI-OPS',
                "X-Title": 'AI-OPS',
            },
            data=json.dumps({
                "model": self.models[self.model],
                "messages": messages,
                # 'stream': True how the fuck works
            })
        )

        try:
            response.raise_for_status()
            output = json.loads(response.text)['choices'][0]['message']['content']
        except requests.exceptions.HTTPError or ConnectError as req_err:
            raise RuntimeError(req_err)
        except json.JSONDecodeError as js_err:
            raise RuntimeError(f'Internal Error: {js_err}')

        return output

    def tool_query(self, messages: list, tools: list | None = None):
        raise NotImplementedError("Tool Calling not available for OpenRouter")


@dataclass
class LLM:
    """LLM interface"""
    model: str
    client_url: str = 'http://localhost:11434'
    provider: Provider = None
    provider_class: Provider = Ollama
    api_key: str | None = None

    def __post_init__(self):
        self.provider = self.provider_class(
            model=self.model,
            client_url=self.client_url,
            api_key=self.api_key
        )

    def query(self, messages: list):
        """Generator that returns response chunks."""
        for chunk in self.provider.query(messages):
            yield chunk

    def tool_query(self, messages: list, tools: list | None = None):
        """"""
        return self.provider.tool_query(messages, tools)
