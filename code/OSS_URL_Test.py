import oss2


# 1. 配置你的阿里云 OSS 账户信息
access_key_id = 'your_access_key'  # 替换为你的 Access Key ID
access_key_secret = 'your_access_key_secret'  # 替换为你的 Access Key Secret
bucket_name = 'hkustgz-uavai-datatest'  # 替换为你的 Bucket 名称
endpoint = 'oss-cn-beijing.aliyuncs.com'  # 替换为你的 Endpoint，例如 'http://oss-cn-hangzhou.aliyuncs.com'

# 配置
auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, endpoint, bucket_name)

# 文件夹路径
prefix = '柑橘病虫害1/柑橘木虱/'

# 获取所有图片的URL
image_urls = []
for obj in oss2.ObjectIterator(bucket, prefix=prefix):
    if obj.key.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # 根据需要添加文件格式
        image_urls.append(bucket.sign_url('GET', obj.key, 3600))  # URL有效期设置为1小时


# 将URL写入txt文件
with open('object_urls_all.txt', 'w') as f:
    for url in image_urls:
        f.write(url + '\n')

# 输出URL
for url in image_urls:
    print(url)
