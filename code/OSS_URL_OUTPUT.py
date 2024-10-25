import oss2
import os
from datetime import datetime

# 1. 配置你的阿里云 OSS 账户信息
access_key_id = 'LTAI5tA7GQs9zJp1v7WQ6hpq'  # 替换为你的 Access Key ID
access_key_secret = 'ZdpTuDO7JVc80lOoEb5C2a6DSt1Wra'  # 替换为你的 Access Key Secret
bucket_name = 'hkustgz-uavai-datatest'  # 替换为你的 Bucket 名称
endpoint = 'oss-cn-beijing.aliyuncs.com'  # 替换为你的 Endpoint，例如 'http://oss-cn-hangzhou.aliyuncs.com'

# 配置
auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, endpoint, bucket_name)

# 文件夹路径
prefix = 'frames/'

# 获取所有图片的URL
image_urls = []
for obj in oss2.ObjectIterator(bucket, prefix=prefix):
    if obj.key.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # 根据需要添加文件格式
        # URL有效期设置为48小时（48 * 60 * 60秒）
        image_urls.append(bucket.sign_url('GET', obj.key, 48 * 60 * 60))

# 创建输出文件名，格式为 {文件夹路径名}_{运行时间}.txt
folder_name = os.path.basename(os.path.normpath(prefix))
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
store_period = 48*60*60
output_file_name = f"{folder_name}_{current_time}_{store_period}.txt"

# 将URL写入txt文件
with open(output_file_name, 'w') as f:
    for url in image_urls:
        f.write(url + '\n')

# 输出URL
for url in image_urls:
    print(url)

print(f'所有URL已保存到 {output_file_name}')
