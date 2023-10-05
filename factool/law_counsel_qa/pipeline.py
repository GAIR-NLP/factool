import json
import yaml
import os
import time
import math
import pdb
from typing import List, Dict

from factool.utils.tool import local_search
from factool.utils.base.pipeline import pipeline

class law_counsel_qa_pipeline(pipeline):
    def __init__(self, foundation_model, snippet_cnt, data_link=None, embed_link=None):
        super().__init__('law_counsel_qa', foundation_model)
        self.tool = local_search(snippet_cnt = snippet_cnt, data_link=data_link, embedding_link=embed_link)
        with open(os.path.join(self.prompts_path, "claim_extraction.yaml"), 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.claim_prompt = data['law_counsel_qa']

        with open(os.path.join(self.prompts_path, 'agreement_verification.yaml'), 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.verification_prompt = data['law_counsel_qa']
    
    async def _claim_extraction(self, prompts, responses):
        messages_list = [
            [
                {"role": "system", "content": self.claim_prompt['system']},
                {"role": "user", "content": self.claim_prompt['user'].format(prompt=prompt, response=response)},
            ]
            for prompt, response in zip(prompts,responses)
        ]
        return await self.chat.async_run(messages_list, List)

    async def _verification(self, claims, prompt, response, related_laws):
        messages_list = [
            [
                {"role": "system", "content": self.verification_prompt['system']},
                {"role": "user", "content": self.verification_prompt['user'].format(claim=claim.get("claim_law"), prompt=prompt, response=response, related_laws=related_laws)},
            ]
            if claim.get("claim_law") is not None else [
                {"role": "system", "content": self.verification_prompt['system']},
                {"role": "user", "content": self.verification_prompt['user'].format(claim=claim.get("claim_logic"), prompt=prompt, response=response, related_laws=related_laws)},
            ] for claim in claims 
        ]
        return await self.chat.async_run(messages_list, dict)
    
    def extract_law_number(self, text):
        start_index = text.find("第")
        end_index = text.find("条", start_index)

        # 提取内容
        if start_index != -1 and end_index != -1:
            extracted_content = text[start_index+1:end_index]
            return "《中华人民共和国民事诉讼法》"+extracted_content
        else:
            return None
    
    async def convert_law_number_to_law(self, law_numbers):
        messages_list = [
            [
                {"role": "system", "content": self.claim_prompt['system']},
                {"role": "user", "content": self.claim_prompt['convert'].format(input=law_number)},
            ]
            for law_number in law_numbers
        ]
        return await self.chat.async_run(messages_list, int)


    async def run_with_tool_live(self, prompts, responses):
        claims_in_responses = await self._claim_extraction(prompts, responses)
        evidences_in_responses = []
        verifications_in_responses = []
        for claims_in_response,prompt,response in zip(claims_in_responses, prompts, responses):
            law_numbers = [self.extract_law_number(claim.get("claim_law")) for claim in claims_in_response if claim.get("claim_law") is not None and self.extract_law_number(claim.get("claim_law")) is not None]
            law_numbers = await self.convert_law_number_to_law(law_numbers)
            law_numbers = [law_number-1 for law_number in law_numbers]
            law_number_laws = self.tool.get_laws_from_index(law_numbers)
            related_laws = await self.tool.search(prompt+response)
            related_laws = [doc['content'] for doc in related_laws]
            for law in law_number_laws:
                if law not in related_laws:
                    related_laws.append(law)
            # related_laws += law_number_laws
            # related_laws = list(set(related_laws))
            related_laws = "".join(["<"+ doc + ">" for doc in related_laws])
            evidences_in_responses.append(related_laws)
            verifications = await self._verification(claims_in_response, prompt, response, related_laws)
            verifications_in_responses.append(verifications)

        return claims_in_responses, evidences_in_responses, verifications_in_responses
    
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

        self.sample_list = [{"prompt": prompt, "response": response, "category": 'law_counsel_qa'} for prompt, response in zip(prompts, responses)]

        for i in range(num_batches):
            #print(i)
            batch_start = i * batch_size
            batch_end = min((i + 1) * batch_size, len(responses))

            claims_in_responses, evidences_in_responses, verifications_in_responses = await self.run_with_tool_live(prompts[batch_start:batch_end],responses[batch_start:batch_end])

            for j, (claims_in_response, evidences_in_response, verifications_in_response) in enumerate(zip(claims_in_responses, evidences_in_responses, verifications_in_responses)):
                index = batch_start + j
                
                # if claims_in_response != None:
                #     for k, claim in enumerate(claims_in_response):
                #         if verifications_in_response[k] != None:
                #             if claim != None:
                #                 #verifications_in_response[k].update({'claim': claim['claim']})
                #                 if claim.get("claim_law") is not None:
                #                     verifications_in_response[k] = {'claim_law': claim['claim_law'],**verifications_in_response[k]}
                #                 else:
                #                     verifications_in_response[k] = {'claim_logic': claim['claim_logic'],**verifications_in_response[k]}
                #             else:
                #                 #verifications_in_response[k].update({'claim': 'None'})
                #                 verifications_in_response[k] = {'claim': 'None',**verifications_in_response[k]}

                self.sample_list[index].update({
                    'claims': claims_in_response,
                    'evidences': evidences_in_response,
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