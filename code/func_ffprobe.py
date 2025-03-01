import subprocess
import json
from datetime import datetime
def get_video_length(video_path):
    cmd = f'data\\tool\\ffprobe -v quiet -print_format json -show_format -show_streams "{video_path}"'
    output = subprocess.check_output(cmd, shell=True)
    output_json = json.loads(output)
    video_length = output_json['format']['duration']
    return float(video_length)
def seconds_to_hhmmss(seconds):
    seconds=float(seconds)
    dt = datetime.utcfromtimestamp(seconds)
    time_str = dt.strftime('%H:%M:%S.%f')[:-3]
    return time_str
def calculate_time_difference(time1, time2):
    format_str = '%H:%M:%S.%f'
    dt1 = datetime.strptime(time1, format_str)
    dt2 = datetime.strptime(time2, format_str)
    time_diff = dt2 - dt1
    return time_diff.total_seconds()
def get_fps(video_path):
    # cmd = f"data\\tool\\ffprobe -v quiet -print_format json -show_format -show_streams {video_path}"
    # output = subprocess.check_output(cmd, shell=True)
    # output_json = json.loads(output)
    # fps=output_json['streams'][0]['r_frame_rate'][0:2]
    # # print(fps)
    # return fps
    cmd = f'data\\tool\\ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1 "{video_path}"'
    output = subprocess.check_output(cmd, shell=True)
    # print(output)
    fps = str(output)[2:4]
    # print(fps)
    return fps
    # video_width = output_json['streams'][0]['width']
    # video_height= output_json['streams'][0]['height']
    # return int(video_width),int(video_height)
def get_ratio(video_path):
    cmd = f'data\\tool\\ffprobe -v quiet -print_format json -show_format -show_streams "{video_path}"'
    output = subprocess.check_output(cmd, shell=True)
    output_json = json.loads(output)
    video_width = output_json['streams'][0]['width']
    video_height= output_json['streams'][0]['height']
    return int(video_width),int(video_height)


def pre_video(video_path):
    # pre_w, pre_h = get_ratio(video_path)
    # new_w = 800
    # new_h = int(pre_h / pre_w * new_w)
    # if new_h>1200:
    #     new_w = 400
    #     new_h = int(pre_h / pre_w * new_w)
    # cmd = f'data\\tool\\ffplay -x {new_w} -y {new_h} {video_path}'
    cmd = f'data\\tool\\ffplay  -y 800 "{video_path}"'
    subprocess.call(cmd, shell=True)

def pre_gif(video_path):
    cmd = f'data\\tool\\ffplay  "{video_path}"'
    subprocess.call(cmd, shell=True)

# def set_time_play():
#     cmd = f'data\\tool\\ffplay  -y 800 "{video_path}"'
#     subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    print(get_fps('C:/Users/83853/Desktop/a.mp4'))

    # x,y=get_ratio('temp/repeate.mp4')
    # print(x,y)
    # return float(video_length)
# video_path = "C:/Users/83853/Desktop/视频素材/视频素材/轨道交通/2023_05010.mp4"
# video_length = get_video_length(video_path)
# print(f"The video length is {video_length} seconds.")
# time1=3.2
# time1=seconds_to_hhmmss(time1)
# # time1 = '00:00:5.6'
# time2 = '00:00:10.2'
# diff = calculate_time_difference(time1, time2)
# print(diff)
# video_path = "test.mp4"
# video_length = get_ratio(video_path)
# seconds = 70
# time_str = seconds_to_hhmmss(seconds)
# print(time_str)
# print(get_fps('out.mp4'))
# print(get_video_length('newnew.mp4'))
# print(get_video_length('test.mp4'))