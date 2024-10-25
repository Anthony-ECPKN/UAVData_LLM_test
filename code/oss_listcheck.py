import oss2
import time

check_period = 5

# 1. 配置你的阿里云 OSS 账户信息
access_key_id = 'LTAI5tA7GQs9zJp1v7WQ6hpq'  # 替换为你的 Access Key ID
access_key_secret = 'ZdpTuDO7JVc80lOoEb5C2a6DSt1Wra'  # 替换为你的 Access Key Secret
bucket_name = 'hkustgz-uavai-datatest'  # 替换为你的 Bucket 名称
endpoint = 'oss-cn-beijing.aliyuncs.com'  # 替换为你的 Endpoint，例如 'http://oss-cn-hangzhou.aliyuncs.com'


# 配置
auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, endpoint, bucket_name)

# 文件夹路径
prefix = 'frames/'  # 例如 'images/'

# 获取当前文件列表
def get_current_files():
    return {obj.key for obj in oss2.ObjectIterator(bucket, prefix=prefix)}

# 初始文件列表
previous_files = get_current_files()

# 定期检查
while True:
    time.sleep(check_period)  # 每check_period秒检查一次
    current_files = get_current_files()
    
    # 找出新增的文件
    new_files = current_files - previous_files
    if new_files:
        print("新出现的文件:")
        for file in new_files:
            print(file)
    
    # 更新之前的文件列表
    previous_files = current_files
