import json
import yaml
import os
import time
import math
import pdb
from typing import List, Dict

from factool.utils.tool import local_search
from factool.utils.base.pipeline import pipeline

class med_counsel_qa_pipeline(pipeline):
    def __init__(self, foundation_model, snippet_cnt, data_link=None, embed_link=None):
        super().__init__('med_counsel_qa', foundation_model)
        self.tool = local_search(snippet_cnt = snippet_cnt, data_link=data_link, embedding_link=embed_link)
        with open(os.path.join(self.prompts_path, "claim_extraction.yaml"), 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.claim_prompt = data['med_counsel_qa']

        with open(os.path.join(self.prompts_path, 'agreement_verification.yaml'), 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.verification_prompt = data['med_counsel_qa']
    
    async def _claim_extraction(self, prompts, responses):
        messages_list = [
            [
                {"role": "system", "content": self.claim_prompt['system']},
                {"role": "user", "content": self.claim_prompt['user'].format(prompt=prompt, response=response)},
            ]
            for prompt, response in zip(prompts,responses)
        ]
        return await self.chat.async_run(messages_list, List)

    async def _verification(self, claims, prompt, response, related_knowledge):
        messages_list = [
            [
                {"role": "system", "content": self.verification_prompt['system']},
                {"role": "user", "content": self.verification_prompt['user'].format(claim=claim, prompt=prompt, response=response, related_knowledge=related_knowledge)},
            ] for claim in claims 
        ]
        return await self.chat.async_run(messages_list, dict)
    
    async def _verification_self_check(self, claims, prompt, response):
        messages_list = [
            [
                {"role": "system", "content": self.verification_prompt['system']},
                {"role": "user", "content": self.verification_prompt['self_check'].format(claim=claim, prompt=prompt, response=response)},
            ] for claim in claims 
        ]
        return await self.chat.async_run(messages_list, dict)

    async def run_with_tool_live(self, prompts, responses):
        claims_in_responses = await self._claim_extraction(prompts, responses)
        evidences_in_responses = []
        verifications_in_responses = []
        for claims_in_response,prompt,response in zip(claims_in_responses, prompts, responses):
            related_knowledge = await self.tool.search(prompt+response)
            related_knowledge = [doc['content'] for doc in related_knowledge]
            related_knowledge = "".join(["<"+ doc + ">" for doc in related_knowledge])
            evidences_in_responses.append(related_knowledge)
            verifications = await self._verification(claims_in_response, prompt, response, related_knowledge)
            verifications_in_responses.append(verifications)

        return claims_in_responses, evidences_in_responses, verifications_in_responses

    async def run_with_tool_live_self_check(self, prompts, responses):
        claims_in_responses = await self._claim_extraction(prompts, responses)
        evidences_in_responses = []
        verifications_in_responses = []
        for claims_in_response,prompt,response in zip(claims_in_responses, prompts, responses):
            verifications = await self._verification_self_check(claims_in_response, prompt, response)
            verifications_in_responses.append(verifications)

        return claims_in_responses, verifications_in_responses
    
    async def run_with_tool_live_without_claim_extraction(self, claims):
        queries = await self._query_generation(claims)
        evidences = await self.tool.run(queries)

        final_response = await self._verification(claims, evidences)
        for i in range(len(final_response)):
            if final_response[i] != None:
                final_response[i]['queries'] = queries[i]
                final_response[i]['evidences'] = evidences[i]

        return final_response
    
    async def run_with_tool_api_call(self, prompts, responses):
        batch_size = 5
        num_batches = math.ceil(len(prompts) / batch_size)

        self.sample_list = [{"prompt": prompt, "response": response, "category": 'med_counsel_qa'} for prompt, response in zip(prompts, responses)]

        for i in range(num_batches):
            #print(i)
            batch_start = i * batch_size
            batch_end = min((i + 1) * batch_size, len(responses))

            claims_in_responses, evidences_in_responses, verifications_in_responses = await self.run_with_tool_live(prompts[batch_start:batch_end],responses[batch_start:batch_end])

            for j, (claims_in_response, evidences_in_response, verifications_in_response) in enumerate(zip(claims_in_responses, evidences_in_responses, verifications_in_responses)):
                index = batch_start + j
                self.sample_list[index].update({
                    'claims': claims_in_response,
                    'evidences': evidences_in_response,
                    'claim_level_factuality': verifications_in_response,
                    'response_level_factuality': all([verification['factuality'] if verification != None else True for verification in verifications_in_response])
                })

        return self.sample_list

    async def run_with_tool_api_call_self_check(self, prompts, responses):
        batch_size = 5
        num_batches = math.ceil(len(prompts) / batch_size)

        self.sample_list = [{"prompt": prompt, "response": response, "category": 'med_counsel_qa'} for prompt, response in zip(prompts, responses)]

        for i in range(num_batches):
            #print(i)
            batch_start = i * batch_size
            batch_end = min((i + 1) * batch_size, len(responses))

            claims_in_responses, verifications_in_responses = await self.run_with_tool_live_self_check(prompts[batch_start:batch_end],responses[batch_start:batch_end])

            for j, (claims_in_response, verifications_in_response) in enumerate(zip(claims_in_responses, verifications_in_responses)):
                index = batch_start + j
                self.sample_list[index].update({
                    'claims': claims_in_response,
                    'claim_level_factuality': verifications_in_response,
                    'response_level_factuality': all([verification['factuality'] if verification != None else True for verification in verifications_in_response])
                })

        return self.sample_list
    
    async def run_with_tool_dataset(self, annotated_dataset_path: str, with_tool_classified_dataset_path: str, rerun: bool = False, rerun_indices: list = []):
        data_path = with_tool_classified_dataset_path if rerun else annotated_dataset_path
        with open(data_path, 'r') as f:
            data = [json.loads(line) for line in f]
        self.sample_list = data if rerun else [claim for sample in data for claim in sample['claims']]
        rerun_elements = self.sample_list if not rerun else [self.sample_list[i] for i in rerun_indices]

        batch_size = 4
        num_batches = math.ceil(len(rerun_elements) / batch_size) # 5
        
        for i in range(num_batches):
            print(i)
            batch_start = i * batch_size
            batch_end = min((i + 1) * batch_size, len(rerun_elements))

            responses = await self.run_with_tool_live_without_claim_extraction(rerun_elements[batch_start:batch_end])

            for j, response in enumerate(responses):
                index = batch_start + j if rerun == False else rerun_indices[batch_start + j]
                if response is None:
                    self.sample_list[index].update({
                        'with_tool_classification': 'None',
                        'with_tool_reasoning': 'None',
                        'queries': 'None',
                        'evidences': 'None'
                    })
                else:
                    self.sample_list[index].update({
                        'with_tool_classification': response.get('factuality', 'None'),
                        'with_tool_reasoning': response.get('reasoning', 'None'),
                        'queries': response.get('queries', 'None'),
                        'evidences': response.get('evidences', 'None')
                    })
        
            # save everything after each batch to prevent data loss
            with open(with_tool_classified_dataset_path, 'w') as f:
                for item in self.sample_list:
                    json_str = json.dumps(item)
                    f.write(json_str + '\n')

    async def run_self_check_live(self, fewshot, batch):
        user_prompt_key = 'user_3_shot_CoT' if fewshot else 'user_zero_shot_CoT'
        messages_list = [
            [
                {"role": "system", "content": self.self_check_prompt['system']},
                {"role": "user", "content": self.self_check_prompt[user_prompt_key].format(claim=response['claim'])},
            ]
            for response in batch
        ]
        return await self.chat.async_run(messages_list, Dict)

    async def run_self_check_dataset(self, annotated_dataset_path: str, self_check_classified_dataset_path: str, fewshot: bool = False, rerun: bool = False, rerun_indices: list = []):
        data_path = annotated_dataset_path if not rerun else self_check_classified_dataset_path
        with open(data_path, 'r') as f:
            data = [json.loads(line) for line in f]
        self.sample_list = data if rerun else [claim for sample in data for claim in sample['claims']]
        rerun_elements = self.sample_list if not rerun else [self.sample_list[i] for i in rerun_indices]

        batch_size = 10
        num_batches = math.ceil(len(rerun_elements) / batch_size)

        for i in range(num_batches):
            print(i)
            batch_start = i * batch_size
            batch_end = min((i + 1) * batch_size, len(rerun_elements))
            batch = rerun_elements[batch_start:batch_end]

            responses = await self.run_self_check_live(fewshot, batch)
            for j, response in enumerate(responses):
                index = batch_start + j if not rerun else rerun_indices[batch_start + j]
                if response is None:
                    self.sample_list[index].update({
                        'self_check_classification': 'None',
                        'self_check_reasoning': 'None'
                    })
                else:
                    self.sample_list[index].update({
                        'self_check_classification': response.get('factuality', 'None'),
                        'self_check_reasoning': response.get('reasoning', 'None')
                    })

            # save everything after each batch to prevent data loss
            with open(self_check_classified_dataset_path, 'w') as f:
                for item in self.sample_list:
                    json_str = json.dumps(item)
                    f.write(json_str + '\n')
