#以下程序需使用python3运行
import os
import oss2
import subprocess
from datetime import datetime


# 1. 配置你的阿里云 OSS 账户信息
access_key_id = 'LTAI5tA7GQs9zJp1v7WQ6hpq'  # 替换为你的 Access Key ID
access_key_secret = 'ZdpTuDO7JVc80lOoEb5C2a6DSt1Wra'  # 替换为你的 Access Key Secret
bucket_name = 'hkustgz-uavai-datatest'  # 替换为你的 Bucket 名称
endpoint = 'oss-cn-beijing.aliyuncs.com'  # 替换为你的 Endpoint，例如 'http://oss-cn-hangzhou.aliyuncs.com'


# 创建OSS授权
auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, endpoint, bucket_name)

def upload_image_to_oss(image_path, object_name):
    bucket.put_object_from_file(object_name, image_path)

def extract_frames_and_upload(video_folder, output_folder, fps=2):
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 遍历视频文件夹中的所有视频文件
    for video_file in os.listdir(video_folder):
        if video_file.endswith(('.mp4', '.avi', '.mov')):  # 根据需要添加文件类型
            video_path = os.path.join(video_folder, video_file)
            # 使用ffmpeg提取帧
            output_pattern = os.path.join(output_folder, f'{video_file}_%04d.jpg')
            command = f'ffmpeg -i "{video_path}" -vf "fps={fps}" "{output_pattern}"'
            subprocess.run(command, shell=True)

            # 上传提取的图片到OSS
            for image_file in os.listdir(output_folder):
                if image_file.startswith(video_file):  # 确保只上传当前视频的帧
                    image_path = os.path.join(output_folder, image_file)
                    upload_image_to_oss(image_path, f'frames/{image_file}')
                    #os.remove(image_path)  # 上传后删除本地文件

def fetch_image_urls_to_txt(auth,bucket,prefix, target_folder):

    # 获取所有图片的URL
    image_urls = []
    store_period = 48
    for obj in oss2.ObjectIterator(bucket, prefix=prefix):
        if obj.key.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # 根据需要添加文件格式
            # URL有效期设置为48小时（48 * 60 * 60秒）
            image_urls.append(bucket.sign_url('GET', obj.key, store_period * 60 * 60))

    # 创建输出文件名，格式为 {文件夹路径名}_{运行时间}.txt
    folder_name = os.path.basename(os.path.normpath(prefix))
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_name = f"{folder_name}_{current_time}_{store_period}.txt"
    output_file_path = os.path.join(target_folder, output_file_name)

    # 将URL写入txt文件
    with open(output_file_path, 'w') as f:
        for url in image_urls:
            f.write(url + '\n')

    # 输出URL
    for url in image_urls:
        print(url)

    print(f'所有URL已保存到 {output_file_path}')

def list_subfolders_in_oss(auth,bucket,target_folder):
    # 获取所有子文件夹
    subfolders = []
    for obj in oss2.ObjectIterator(bucket, prefix=target_folder, delimiter='/'):
        if obj.is_prefix():  # 判断是否为子文件夹
            subfolders.append(obj.key)

    return subfolders

# 示例
video_path = 'Data/Video/'  # 视频文件的路径
target_folder = 'Data/Video/picture_output/'  # 输出图片的目标文件夹
extract_frames_and_upload(video_path, target_folder) #将视频中的图片拆帧并存储在目标文件夹，同时所有图片上传到prefix文件夹

#接下来生成目标云盘文件夹的所有对应url链接文件
# 文件夹路径
prefix = 'frames/'
oss_folders =list_subfolders_in_oss(auth,bucket,prefix) 

# 输出子文件夹名称
for folder in oss_folders:
    fetch_image_urls_to_txt(auth,bucket,folder,'Data_URL_list')
    print(folder)

