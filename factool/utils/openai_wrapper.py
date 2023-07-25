# the async version is adapted from https://gist.github.com/neubig/80de662fb3e225c18172ec218be4917a

from __future__ import annotations

import os
import yaml
import openai
import ast
import pdb
import asyncio
from typing import Any, List
import os
import pathlib


from factool.env_config import factool_env_config

# env
openai.api_key = factool_env_config.openai_api_key

class OpenAIChat():
    def __init__(
            self,
            model_name='gpt-3.5-turbo',
            max_tokens=2500,
            temperature=0,
            top_p=1,
            request_timeout=60,
    ):
        self.config = {
            'model_name': model_name,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p,
            'request_timeout': request_timeout,
        }

    
    def _boolean_fix(self, output):
        return output.replace("true", "True").replace("false", "False")

    def _type_check(self, output, expected_type):
        try:
            output_eval = ast.literal_eval(output)
            if not isinstance(output_eval, expected_type):
                return None
            return output_eval
        except:
            return None

    async def dispatch_openai_requests(
        self,
        messages_list,
    ) -> list[str]:
        """Dispatches requests to OpenAI API asynchronously.
        
        Args:
            messages_list: List of messages to be sent to OpenAI ChatCompletion API.
        Returns:
            List of responses from OpenAI API.
        """
        async def _request_with_retry(messages, retry=3):
            for _ in range(retry):
                try:
                    response = await openai.ChatCompletion.acreate(
                        model=self.config['model_name'],
                        messages=messages,
                        max_tokens=self.config['max_tokens'],
                        temperature=self.config['temperature'],
                        top_p=self.config['top_p'],
                        request_timeout=self.config['request_timeout'],
                    )
                    return response
                except openai.error.RateLimitError:
                    print('Rate limit error, waiting for 40 second...')
                    await asyncio.sleep(40)
                except openai.error.APIError:
                    print('API error, waiting for 1 second...')
                    await asyncio.sleep(1)
                except openai.error.Timeout:
                    print('Timeout error, waiting for 1 second...')
                    await asyncio.sleep(1)
                except openai.error.ServiceUnavailableError:
                    print('Service unavailable error, waiting for 3 second...')
                    await asyncio.sleep(3)
            return None

        async_responses = [
            _request_with_retry(messages)
            for messages in messages_list
        ]

        return await asyncio.gather(*async_responses)
    
    async def async_run(self, messages_list, expected_type):
        retry = 1
        responses = [None for _ in range(len(messages_list))]
        messages_list_cur_index = [i for i in range(len(messages_list))]

        while retry > 0 and len(messages_list_cur_index) > 0:
            print(f'{retry} retry left...')
            messages_list_cur = [messages_list[i] for i in messages_list_cur_index]
            
            predictions = await self.dispatch_openai_requests(
                messages_list=messages_list_cur,
            )

            preds = [self._type_check(self._boolean_fix(prediction['choices'][0]['message']['content']), expected_type) if prediction is not None else None for prediction in predictions]

            finised_index = []
            for i, pred in enumerate(preds):
                if pred is not None:
                    responses[messages_list_cur_index[i]] = pred
                    finised_index.append(messages_list_cur_index[i])
            
            messages_list_cur_index = [i for i in messages_list_cur_index if i not in finised_index]
            
            retry -= 1
        
        return responses

if __name__ == "__main__":
    chat = OpenAIChat()

    predictions = chat.async_run(
        messages_list=[
            [{"role": "user", "content": "show either 'ab' or '['a']'. Do not do anything else."}],
        ] * 20,
        expected_type=List,
    )