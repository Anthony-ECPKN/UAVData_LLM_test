###以下是一个脚本，用于导出 Data_vlm_responses 文件夹下指定 .json 文件中的所有 content 条目的信息

import json
import os

def extract_content_from_json(json_file_path, output_txt_path):
    # 读取 JSON 文件
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # 提取 content 信息
    contents = [entry['content'] for entry in data if 'content' in entry]

    # 将 content 信息写入 TXT 文件
    with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
        for content in contents:
            print(content)
            txt_file.write(content + '\n')

    print(f'内容已保存到 {output_txt_path}')

# 示例调用
json_file_path = 'Data_vlm_responses/glm-4v-plus_20240929_022547_object_urls_samples.json'  # 替换为你的文件名
output_txt_path = 'Data_vlm_responses/contents_output.txt'  # 输出文件路径
extract_content_from_json(json_file_path, output_txt_path)
