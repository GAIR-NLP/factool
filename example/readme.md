# An example of med_doc_qa
## Input data
### dialogue
> 医生：你好，我是你的主治医生。请详细描述一下你的不适症状，包括症状的持续时间、频率以及伴随的其他感觉 </br>
患者：我最近总感觉头晕，有时候还会有心慌的感觉，这种情况大概持续了一个月左右，每周会出现两三次。</br>
医生：你有测量过血压吗？如果有，能告诉我最近一次的测量结果吗？</br>
患者：我自己在家测过，大概在150/100mmHg左右。</br>
医生：你的血压偏高，这可能是引起你头晕和心慌的原因。你有没有其他的不适症状，比如头痛、胸闷、呼吸困难或者视物模糊等？</br>
患者：我有时候会有点头痛，但是并不严重，胸闷和呼吸困难倒是没有，视物也没有模糊。</br>
医生：你有没有长期服用降压药或者有高血压的病史？你的家族中有没有高血压病史？</br>
患者：我父母都有高血压，我自己以前也有过，但是后来控制得还不错，就没有再吃药了。</br>
医生：你的生活习惯怎么样？比如饮食、运动、睡眠等。你的工作压力大吗？有没有经常熬夜或者加班的情况？</br>
患者：我平时工作比较忙，经常加班，饮食不是很规律，运动也比较少，有时候晚上睡觉也不是很好。</br>
医生：你的生活习惯可能是导致血压升高的一个重要因素，建议你调整一下。你有没有吸烟、饮酒的习惯？</br>
患者：我有吸烟，但是饮酒就很少。</br>
医生：吸烟也是导致血压升高的一个重要因素，建议你尽量戒烟。你的血压已经达到了高血压的标准，需要及时治疗。高血压是心脑血管疾病的重要危险因素，如果不及时控制，可能会引发心脏病、脑卒中等严重疾病。</br>
患者：那我应该怎么做呢？</br>
医生：首先，你需要调整生活习惯，规律饮食，适当运动，保证充足的睡眠，尽量戒烟。其次，你需要定期测量血压，如果血压持续偏高，可能需要服用降压药。我会为你制定一个详细的治疗方案，包括药物治疗和生活方式的调整，我们会定期复查，根据你的病情调整治疗方案。</br>
患者：好的，我知道了，谢谢医生。

### wrong medical record
> 主诉：头晕、心慌，持续一个月，每周出现两三次，偶尔伴有轻微头痛。</br>
现病史：患者最近一个月内经常感到头晕和心慌，每周出现两三次，自测血压160/110mmHg，偶尔伴有轻微头痛，无胸闷、呼吸困难等症状。</br>
既往史：患者有高血压病史，父母均有高血压，患者曾因血压控制良好而停药，无糖尿病、心脏病等病史。</br>
个人史：患者工作压力大，经常加班，饮食不规律，运动少，睡眠质量差，有吸烟习惯，饮酒少。</br>
诊断：高血压病，考虑为二级高血压。</br>
治疗建议：</br>
1.调整生活习惯，规律饮食，适当运动，保证充足的睡眠，尽量戒烟。</br>
2.定期测量血压，如果血压持续偏高，可能需要服用降压药。</br>
3.制定详细的治疗方案，包括药物治疗和生活方式的调整，定期复查，根据病情调整治疗方案。</br>
4.建议服用降压药物，如无不适，继续服用。

### wrong points
1. 现病史中“160/110mmHg”为错误信息
2. 既往史中“无糖尿病、心脏病等病史”为多余信息。
3. 诊断中“考虑为二级高血压”为多余信息。
4. 治疗建议中“建议服用降压药物，如无不适，继续服用”为多余信息

### factool claim level factuality output(using the code snippet example.py)
~~~python
[{"claim": "主诉是头晕、心慌，持续一个月，每周出现两三次，偶尔伴有轻微头痛", "reasoning": "给定的文本与提供的证据完全一致。文本中的信息，包括患者的主诉（头晕、心慌，持续一个月，每周出现两三次，偶尔伴有轻微头痛）都在证据中得到了确认。", "error": "None", "correction": "None", "factuality": true}, 
{"claim": "现病史包含最近一个月内经常感到头晕和心慌，每周出现两三次", "reasoning": "根据提供的证据，患者确实描述了他在过去一个月内经常感到头晕和心慌，每周出现两三次的症状。这与给定的文本完全一致。", "error": "None", "correction": "None", "factuality": true}, 
{"claim": "现病史包含自测血压160/110mmHg", "reasoning": "根据提供的证据，患者自测的血压值是150/100mmHg，而不是文本中所述的160/110mmHg。", "error": "文本中的血压值与证据中的血压值不符。", "correction": "现病史包含自测血压150/100mmHg", "factuality": false}, 
{"claim": "现病史包含偶尔伴有轻微头痛，无胸闷、呼吸困难等症状", "reasoning": "根据证据，患者确实有偶尔的轻微头痛，但并没有胸闷和呼吸困难的症状。因此，给定的文本是事实。", "error": "None", "correction": "None", "factuality": true}, 
{"claim": "既往史包含有高血压病史，父母均有高血压", "reasoning": "根据提供的证据，患者的既往史确实包含有高血压病史，他的父母也都有高血压。这与给定的文本中的信息完全一致。", "error": "None", "correction": "None", "factuality": true}, 
{"claim": "既往史包含曾因血压控制良好而停药，无糖尿病、心脏病等病史", "reasoning": "根据证据，患者曾经有过高血压，但后来控制得还不错，所以停止了药物治疗。这与文本中的描述一致。然而，文本中的描述“无糖尿病、心脏病等病史”在证据中并未提及，因此无法确认其准确性。", "error": "文本中的“无糖尿病、心脏病等病史”是擅自增加的信息，证据中并未提及。", "correction": "既往史包含曾因血压控制良好而停药", "factuality": false}, 
{"claim": "个人史包含工作压力大，经常加班，饮食不规律，运动少，睡眠质量差，有吸烟习惯，饮酒少", "reasoning": "根据提供的证据，患者的个人史包括工作压力大，经常加班，饮食不规律，运动少，睡眠质量差，有吸烟习惯，饮酒少。这与给定的文本完全一致。", "error": "None", "correction": "None", "factuality": true}, 
{"claim": "诊断为高血压病，考虑为二级高血压", "reasoning": "根据提供的证据，患者的血压测量结果为150/100mmHg，医生也确认了患者的血压偏高，这符合高血压的诊断标准。但是，证据中并没有明确指出患者的高血压是二级高血压。", "error": "文本中的错误是擅自增加了对话中没出现的信息，即患者的高血压被诊断为二级高血压。", "correction": "诊断为高血压病", "factuality": false}, 
{"claim": "治疗建议包括调整生活习惯，规律饮食，适当运动，保证充足的睡眠，尽量戒烟", "reasoning": "给定的文本是事实的。这是因为在证据中，医生确实建议患者调整生活习惯，规律饮食，适当运动，保证充足的睡眠，尽量戒烟。这些都是医生为了帮助患者控制高血压而给出的建议。", "error": "None", "correction": "None", "factuality": true}, 
{"claim": "治疗建议包括定期测量血压，如果血压持续偏高，可能需要服用降压药", "reasoning": "给定的文本与提供的证据完全一致。在证据中，医生确实建议患者定期测量血压，并且如果血压持续偏高，可能需要服用降压药。", "error": "None", "correction": "None", "factuality": true}, 
{"claim": "治疗建议包括制定详细的治疗方案，包括药物治疗和生活方式的调整，定期复查，根据病情调整治疗方案", "reasoning": "给定的文本与提供的证据完全一致。在证据中，医生确实为患者制定了一个详细的治疗方案，包括药物治疗和生活方式的调整，并且提到了定期复查，根据病情调整治疗方案。", "error": "None", "correction": "None", "factuality": true}, 
{"claim": "治疗建议包括建议服用降压药物，如无不适，继续服用", "reasoning": "根据提供的证据，医生确实建议患者如果血压持续偏高，可能需要服用降压药。同时，医生也建议患者在没有不适的情况下继续服用。因此，给定的文本是事实。", "error": "None", "correction": "None", "factuality": true}]
~~~
### the revised medical record based on the factuality test output
> 主诉：头晕、心慌，持续一个月，每周出现两三次，偶尔伴有轻微头痛。</br>现病史：患者最近一个月内经常感到头晕和心慌，自测血压150/100mmHg，无胸闷、呼吸困难等症状。</br>既往史：患者有高血压病史，父母均有高血压，曾因血压控制良好而停药。</br>个人史：患者工作压力大，经常加班，饮食不规律，运动少，睡眠质量差，有吸烟习惯，饮酒少。</br>诊断：高血压病。</br>治疗建议：</br>1.调整生活习惯，规律饮食，适当运动，保证充足的睡眠，尽量戒烟。</br>2.定期测量血压，如果血压持续偏高，可能需要服用降压药。</br>3.制定详细的治疗方案，包括药物治疗和生活方式的调整，定期复查，根据病情调整治疗方案。</br>4.建议服用降压药物，如无不适，继续服用。

共修正三处错误，一处错误未识别
