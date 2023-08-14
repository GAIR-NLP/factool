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
                "prompt":"""患者:从上个月开始嘴角就一直有一点疼疼的，你看这是什么原因呢？
医生:嘴角疼痛可能是嘴角炎或是缺乏一些维生素，你平时有注意口腔卫生吗？
患者:口腔卫生挺注意的，每天都刷牙，用牙线清理。
患者:就是最近工作压力有点大，经常吃一些快餐和外卖。
医生:有没有最近因为吃东西不注意导致口角破裂？
患者:这个好像没有注意到，只是有一两次吃饭时嘴角稍微疼了一下。
医生:那我们就暂且定为嘴角炎，我建议你可以试试涂一些口腔护理药膏，如果过几天情况有明显改善，应该就是嘴角炎引起的。
患者:那维生素的话要补充吗？
医生:嗯，维生素B2和B6对于舌炎和嘴角炎有一些好处，你可以适当的补充一些。
患者:一般每天怎么补充？有没有推荐的食物或者药品？
医生:我们一般建议在药店买一些维生素B2和B6的药片服用，平时你也可以多吃一些绿色蔬菜，豆类及坚果类食物，他们都比较富含这两种维生素。
患者:好，我知道了，多谢医生。""",
                "response":"""主诉：上个月开始头痛频繁
现病史：从上个月开始，患者嘴角疼痛，无破损症状。近期工作压力大，饮食习惯改变，经常吃快餐和外卖，此外还有过度咖啡因摄入的习惯。
既往史：患者以前有高血压的病史。
诊断：口腔疾病—嘴角炎。
治疗建议：
1. 使用口腔护理药膏，早晚各一次，添加使用抗生素治疗。
2. 适当补充维生素B2和B6，方法是吃绿色蔬菜、豆类及坚果类食物或药店购买口服，并额外补充维生素D。
3. 注意口腔卫生，减少吃快餐和外卖，同时要戒掉喝咖啡的习惯。
4. 尽量减小工作压力，保持良好心态。""",
                "category": "med_doc_qa",
            }
]

response_list = factool_instance.run(inputs)

print(response_list)