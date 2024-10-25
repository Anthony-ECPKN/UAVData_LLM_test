import os
import oss2
import subprocess

# 1. 配置你的阿里云 OSS 账户信息
access_key_id = 'your_access_key'  # 替换为你的 Access Key ID
access_key_secret = 'your_access_key_secret'  # 替换为你的 Access Key Secret
bucket_name = 'hkustgz-uavai-datatest'  # 替换为你的 Bucket 名称
endpoint = 'oss-cn-beijing.aliyuncs.com'  # 替换为你的 Endpoint

# 创建OSS授权
auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, endpoint, bucket_name)

def upload_image_to_oss(image_path, object_name):
    bucket.put_object_from_file(object_name, image_path)

def extract_frames_and_upload(video_folder, outputfolder, fps=2):
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)
    # 遍历视频文件夹中的所有视频文件
    for video_file in os.listdir(video_folder):
        if video_file.endswith(('.mp4', '.avi', '.mov')):  # 根据需要添加文件类型
            video_path = os.path.join(video_folder, video_file)

            # 创建以视频名称命名的OSS文件夹
            video_name = os.path.splitext(video_file)[0]  # 获取视频文件名（不带扩展名）
            oss_folder = f'frames/{video_name}/'
            
            # 使用ffmpeg提取帧
            output_pattern = os.path.join(output_folder, f'{video_file}_%04d.jpg')
            #output_pattern = f'{video_name}_%04d.jpg'
            command = f'ffmpeg -i "{video_path}" -vf "fps={fps}" "{output_pattern}"'
            subprocess.run(command, shell=True)

            # 上传提取的图片到OSS
            for image_file in os.listdir(output_folder):
                if image_file.startswith(video_file):  # 确保只上传当前视频的帧
                    image_path = os.path.join(output_folder, image_file)
                    upload_image_to_oss(image_path, f'frames/{image_file}')
                    #os.remove(image_path)  # 上传后删除本地文件

# 示例
video_path = 'Data/Video/Video_test'  # 视频文件的路径
target_folder = 'Data/Video/picture_output/'  # 输出图片的目标文件夹
extract_frames_and_upload(video_path, target_folder,fps = 0.1)

