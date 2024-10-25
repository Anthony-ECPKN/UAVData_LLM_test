###
#函数输入为两项，分别为要分析的对应种类的所有图片url链接，以及VLM分析结果要存放的文件夹。
#函数输出.json文件，包含了对每个文件夹图片的的分析回答，问题为:判断图中植物是否含有病虫害。若存在病虫害，请说明对应种类。

import json
from zhipuai import ZhipuAI
from datetime import datetime
import os
import oss2

def process_image_urls_to_json(url_file_name, output_folder):
    client = ZhipuAI(api_key="your_key")  # 填写您自己的APIKey

    # 读取URL
    with open(url_file_name, 'r') as f:
        urls = f.readlines()
        print(urls)

    # 存储所有回复
    responses = []

    # 对每个URL进行访问
    for url in urls:
        url = url.strip()  # 去掉换行符
        print(url)
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
                            #"text": "判断图中植物是否含有病虫害。若存在病虫害，请说明对应种类。"
                            "text": "图中有什么"
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

    folder_name = 'Data_URL_list'  # 你要去掉的文件夹名
    new_name = url_file_name.replace(f"{folder_name}/", "")  # 结果为 'object_urls_test.txt'
    new_name_without_extension = new_name.replace('.txt', '')  # 结果为 'object_urls_test'
    json_file_name = f"{model_name}_{current_time}_{new_name_without_extension}.json"
    json_file_path = os.path.join(output_folder, json_file_name)

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 保存为JSON文件
    try:
        with open(json_file_path, 'w') as json_file:
            json.dump(responses, json_file, ensure_ascii=False, indent=2)
        print(f'所有回复已保存到 {json_file_path}')
    except Exception as e:
        print(f"保存JSON文件时出错: {e}")

# 示例调用

process_image_urls_to_json('Data_URL_list/frames_20241008_110844_172800.txt', 'Data_vlm_responses')

