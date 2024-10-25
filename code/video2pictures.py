import subprocess

def extract_frames(video_path, output_pattern, fps=0.1):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f'fps={fps}',
        output_pattern
    ]
    subprocess.run(command)

# 示例用法
video_path = 'Data/Video/FPV_test.mp4'  # 视频文件的路径
target_folder = 'Data/Video/picture_output/output_frame_%04d.jpg'  # 输出图片的目标文件夹
extract_frames(video_path, target_folder, fps=0.1)