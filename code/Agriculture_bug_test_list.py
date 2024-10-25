import json
from zhipuai import ZhipuAI
from datetime import datetime

client = ZhipuAI(api_key="e7cb4f57c94a8bbe9bb600a78fd0933d.00bhOFe4NY3t8ES9")  # 填写您自己的APIKey

# 读取URL
url_file_name = 'object_urls_all.txt'
#url_file_name = 'object_urls_samples.txt'
with open(url_file_name, 'r') as f:
    urls = f.readlines()

# 存储所有回复
responses = []

# 对每个URL进行访问
for url in urls:
    url = url.strip()  # 去掉换行符
    response = client.chat.completions.create(
        model="glm-4v-plus",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": url
                        }
                    },
                    {
                        "type": "text",
                        "text": "判断图中植物是否含有病虫害。若存在病虫害，请说明对应种类。"
                    }
                ]
            }
        ]
    )
    # 将单个回复添加到列表中，转换为字典格式
    responses.append({
        "content": response.choices[0].message.content,
        "role": response.choices[0].message.role
    })
    print(response.choices[0].message.content)

# 创建JSON文件名
model_name = "glm-4v-plus"
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
json_file_name = f"{model_name}_{current_time}_{url_file_name.replace('.txt', '')}.json"

# 保存为JSON文件
with open(json_file_name, 'w') as json_file:
    json.dump(responses, json_file, ensure_ascii=False, indent=2)

print(f'所有回复已保存到 {json_file_name}')