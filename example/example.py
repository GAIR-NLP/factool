'''
Remember to export you API keys first.
export OPENAI_API_KEY=...
export SERPER_API_KEY=...
export SCRAPER_API_KEY=...
'''

from factool import Factool

factool_instance = Factool("gpt-4")

# one example input for each category.
inputs = [
            {
                "prompt": "Introduce Graham Neubig",
                "response": "Graham Neubig is a professor at MIT",
                "category": "kbqa"
            },
            {
                "prompt": "def get_max_triples(n): \"\"\" You are given a positive integer n. You have to create an integer array a of length n. For each i (1 \u2264 i \u2264 n), the value of a[i] = i * i - i + 1. Return the number of triples (a[i], a[j], a[k]) of a where i < j < k, and a[i] + a[j] + a[k] is a multiple of 3. Example : Input: n = 5 Output: 1 Explanation: a = [1, 3, 7, 13, 21] The only valid triple is (1, 7, 13). \"\"\" Now implement the function get_max_triples using Python",
                "response": "def get_max_triples(n):\n    a = [i * i - i + 1 for i in range(1, n+1)]\n    count = 0\n    for i in range(n-2):\n        for j in range(i+1, n-1):\n            for k in range(j+1, n):\n                if (a[i] + a[j] + a[k]) % 3 == 0:\n                    count += 1\n    return count\n\nprint(get_max_triples(5)) # Output: 1",
                "category": "code",
                "entry_point": "get_max_triples"
            },
            {
                "prompt": "Stephen placed an online order for groceries.  His final bill came to $7023116.  Because this was through a delivery vendor, they tacked on a 25% fee to his final total and charged him $3.00 in delivery fees.  Stephen also added a $4.00 tip.  After the extra fees, what was the final price of Stephen's groceries?",
                "response": "Okay, here are the steps to solve this:\n* Stephen's initial grocery bill was $7023116\n* The delivery vendor charged a 25% fee on top of that. 25% of $7023116 is 0.25 * $7023116 = $1755779\n* They also charged a flat $3 delivery fee\n* Stephen added a $4 tip\n* So the total charges were:\n    * Initial groceries: $7023116\n    * 25% fee: $1755779\n    * Delivery fee: $3 \n    * Tip: $4\n* Adding all that up, the total final price was $7023116 + $1755779 + $3 + $4 = $8779902\n\nSo the final price of Stephen's groceries was $8779902",
                "category": "math"
            },
            {
                "prompt": "Detail how machine learning algorithms are applied in data"
                      " analytics and the processes involved in training"
                      " these algorithms. Please cite relevant research papers"
                      " or textbooks to support your points, including the author's"
                      " name, the title of the work, and the year of publication.",
                "response": "Machine learning algorithms play a crucial role in data"
                        " analytics. They are used to extract insights and knowledge"
                        " from large datasets, which can be used to make informed"
                        " decisions and predictions. The following are the processes"
                        " involved in training machine learning algorithms:\n\n1. "
                        "Data Preprocessing: The first step in training a machine"
                        " learning algorithm is to preprocess the data. This involves"
                        " cleaning the data, handling missing values, "
                        "encoding categorical variables, and scaling the data. "
                        "The aim of preprocessing is to ensure that the data is in"
                        " a format that can be used by the machine learning algorithm.\n2. Feature Selection: Once the data has been preprocessed, the next step is to select the relevant features that will be used to train the machine learning algorithm. This involves identifying the features that are most important for predicting the target variable. Feature selection can be done using various techniques, such as filter methods, wrapper methods, and embedded methods.\n3. Model Selection: After feature selection, the next step is to select the appropriate machine learning algorithm to use. There are various types of machine learning algorithms, such as supervised learning, unsupervised learning, and reinforcement learning. The choice of algorithm depends on the nature of the problem and the type of data available.\n4. Training the Model: Once the model has been selected, the next step is to train the machine learning algorithm using the preprocessed data. This involves using a training set of data to optimize the parameters of the model so that it can accurately predict the target variable.\n5. Model Evaluation: After the model has been trained, the next step is to evaluate its performance. This involves testing the model on a separate test set of data and measuring its accuracy, precision, recall, and other performance metrics.\n6. Model Deployment: Once the model has been evaluated and fine-tuned, it can be deployed in a production environment. This involves integrating the model into a larger system or workflow, and monitoring its performance over time.\n\nResearch papers and textbooks that support the above points include:\n\n* \"An Introduction to Machine Learning\" by Alpaydin, B., (2010) which provides a comprehensive overview of machine learning algorithms and their applications.\n* \"Data Mining: Concepts and Techniques\" by Han, J., Kamber, B., & Pei, J., (2011) which provides a detailed introduction to data mining and its applications.\n* \"Machine Learning: Trends, Perspectives, and Prospects\" by Kamber, B., & Pei, J., (2012) which provides an overview of the current trends and future prospects of machine learning.\n* \"Machine Learning for Data Mining\" by He, C., & Wang, Y., (2015) which provides an in-depth introduction to machine learning algorithms and their applications in data mining.",
                "category": "scientific"
            },
            {
                "prompt":"""医生：你好，我是你的主治医生。请详细描述一下你的不适症状，包括症状的持续时间、频率以及伴随的其他感觉。
患者：我最近总感觉头晕，有时候还会有心慌的感觉，这种情况大概持续了一个月左右，每周会出现两三次。
医生：你有测量过血压吗？如果有，能告诉我最近一次的测量结果吗？
患者：我自己在家测过，大概在150/100mmHg左右。
医生：你的血压偏高，这可能是引起你头晕和心慌的原因。你有没有其他的不适症状，比如头痛、胸闷、呼吸困难或者视物模糊等？
患者：我有时候会有点头痛，但是并不严重，胸闷和呼吸困难倒是没有，视物也没有模糊。
医生：你有没有长期服用降压药或者有高血压的病史？你的家族中有没有高血压病史？
患者：我父母都有高血压，我自己以前也有过，但是后来控制得还不错，就没有再吃药了。
医生：你的生活习惯怎么样？比如饮食、运动、睡眠等。你的工作压力大吗？有没有经常熬夜或者加班的情况？
患者：我平时工作比较忙，经常加班，饮食不是很规律，运动也比较少，有时候晚上睡觉也不是很好。
医生：你的生活习惯可能是导致血压升高的一个重要因素，建议你调整一下。你有没有吸烟、饮酒的习惯？
患者：我有吸烟，但是饮酒就很少。
医生：吸烟也是导致血压升高的一个重要因素，建议你尽量戒烟。你的血压已经达到了高血压的标准，需要及时治疗。高血压是心脑血管疾病的重要危险因素，如果不及时控制，可能会引发心脏病、脑卒中等严重疾病。
患者：那我应该怎么做呢？
医生：首先，你需要调整生活习惯，规律饮食，适当运动，保证充足的睡眠，尽量戒烟。其次，你需要定期测量血压，如果血压持续偏高，可能需要服用降压药。我会为你制定一个详细的治疗方案，包括药物治疗和生活方式的调整，我们会定期复查，根据你的病情调整治疗方案。
患者：好的，我知道了，谢谢医生。""",
                "response":"""主诉：头晕、心慌，持续一个月，每周出现两三次，偶尔伴有轻微头痛。
现病史：患者最近一个月内经常感到头晕和心慌，每周出现两三次，自测血压160/110mmHg，偶尔伴有轻微头痛，无胸闷、呼吸困难等症状。
既往史：患者有高血压病史，父母均有高血压，患者曾因血压控制良好而停药，无糖尿病、心脏病等病史。
个人史：患者工作压力大，经常加班，饮食不规律，运动少，睡眠质量差，有吸烟习惯，饮酒少。
诊断：高血压病，考虑为二级高血压。
治疗建议：
1.调整生活习惯，规律饮食，适当运动，保证充足的睡眠，尽量戒烟。
2.定期测量血压，如果血压持续偏高，可能需要服用降压药。
3.制定详细的治疗方案，包括药物治疗和生活方式的调整，定期复查，根据病情调整治疗方案。
4.建议服用降压药物，如无不适，继续服用。""",
                "category": "med_doc_qa",
            }
]

response_list = factool_instance.run(inputs)

print(response_list)