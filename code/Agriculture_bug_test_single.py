from zhipuai import ZhipuAI

client = ZhipuAI(api_key="your_key") # 填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4v-plus",  # 填写需要调用的模型名称
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "image_url",
            "image_url": {
                "url" : "https://hkustgz-uavai-datatest.oss-cn-beijing.aliyuncs.com/Data/%E6%9F%91%E6%A9%98%E7%97%85%E8%99%AB%E5%AE%B31/%E6%9F%91%E6%A9%98%E6%9C%A8%E8%99%B1/IMG_20230702_165754.jpg"
            }
          },
          {
            "type": "text",
            "text": "判断图中是否含有虫害，并阐述分析"
          }
        ]
      }
    ]
)
print(response.choices[0].message)
