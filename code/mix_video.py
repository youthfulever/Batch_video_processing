import random
import subprocess
import time

from func_ffprobe import get_video_length


def get_part_time(video_long_time=20, video_min_time=3, video_max_time=6):
    # video_long_time 输出视频最短时间
    time_list = []
    time_sum = 0
    while time_sum < video_long_time:
        time_item = random.uniform(video_min_time, video_max_time)
        time_item = round(time_item, 1)
        # print(time_item)
        time_sum += time_item
        time_list.append(time_item)
    # print(time_list, time_sum)
    return time_list
    # time_list[-1]=video_long_time-(time_sum-time_list[-1])
    # time_sum=0
    # for i in time_list:
    #     time_sum+=i
    # print(time_list,time_sum)


def grab_balls(balls, num_to_grab):
    if num_to_grab > len(balls):
        return -1
    grabbed_balls = []
    for _ in range(num_to_grab):
        ball = random.choice(balls)
        grabbed_balls.append(ball)
        balls.remove(ball)

    return grabbed_balls


def mix(all_balls=['1', '2'],
        video_long_time=20,
        video_min_time=1,
        video_max_time=6,
        video_count=10):
    for i in range(video_count):
        temp_balls = all_balls.copy()
        time_list = get_part_time(video_long_time=video_long_time, video_min_time=video_min_time,
                                  video_max_time=video_max_time)
        video_result = grab_balls(temp_balls, len(time_list))
        # print(time_list, video_result)  # 视频视频，视频列表
        get_start_end_time(time_list, video_result)


def get_start_end_time(time_list, video_result):
    start_end_list = []
    for i in range(len(time_list)):
        temp_dic = {
            'start': '',
            'end': '',
        }
        video_long_time = get_video_length(video_result[i])
        if (video_long_time <= time_list[i]):
            temp_dic['start'] = 0
            temp_dic['end'] = video_long_time
        else:
            start_time = random.uniform(0, video_long_time - time_list[i])
            start_time = round(start_time, 1)
            temp_dic['start'] = start_time
            temp_dic['end'] = start_time + time_list[i]
        start_end_list.append(temp_dic)
    # print(start_end_list)
    merge_video(start_end_list, video_result)


def merge_video(start_end_list, video_result=[], ratio_w=1080, ratio_h=1920, audio_able='0', transitions_flag='1',
                transitions_value='1'):
    in_str = ''
    scale_str = ''
    merge_str = ''
    transitions_value = float(transitions_value) / 2
    print(transitions_value)
    audio_dic = {
        '0': ' -an ',
        '1': ''
    }

    for i in range(len(video_result)):
        transitions_dic = {
            '0': '',
            '1': f',fade=in:st=0:d={transitions_value},fade=out:st={start_end_list[i]["end"] - start_end_list[i]["start"] - transitions_value}:d={transitions_value}'
        }
        in_str += f' -i "{video_result[i]}" '
        scale_str += f'[{i}:v]scale={ratio_w}:{ratio_h}:force_original_aspect_ratio=decrease,pad={ratio_w}:{ratio_h}:(ow-iw)/2:(oh-ih)/2,setsar=1,trim=start={start_end_list[i]["start"]}:end={start_end_list[i]["end"]},setpts=PTS-STARTPTS{transitions_dic[transitions_flag]}[new{i}v];[{i}:a]atrim=start={start_end_list[i]["start"]}:end={start_end_list[i]["end"]},asetpts=PTS-STARTPTS[new{i}a];'
        merge_str += f'[new{i}v][new{i}a]'
    filter_complex_str = f'-filter_complex "{scale_str}{merge_str}concat=n={len(video_result)}:v=1:a=1[vvv][outa];[vvv]fps=30[outv]"'

    command = [
        'data\\tool\\ffmpeg',
        in_str,
        filter_complex_str,
        # f'temp/{str(time.time())[-5:]}.mp4',  # 输出视频
        # audio_dic[audio_able],
        '-map "[outv]" -map "[outa]"',
        f'temp/{str(time.time())[0:10]}.mp4',  # 输出视频
        '-y'
    ]

    command = [x for x in command if x]  # 删除空元素
    command_str = ' '.join(command)
    # print(command_str)
    # print('ddddd1' * 20)
    subprocess.call(command_str, shell=True)


from func_pic import get_crop_ratio_pic


def pictovideo():
    get_crop_ratio_pic(pic_file='shu.jpg', ration_h=1920, ration_w=1080)
    filter_complex = ''' -filter_complex "[0:0]scale=8000:-1,zoompan=z='zoom+0.001':x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=5*60:s=1280*1920:fps=60" '''
    command = f'data\\tool\\ffmpeg -loop 1 -framerate 60 -i temp/mask.jpg {filter_complex} -c:v libx264 -t 10 temp/output_video.mp4 -y'
    # command=f'ffmpeg -loop 1 -framerate 60 -i temp/mask.jpg -c:v libx264 -t 10 temp/output_video.mp4 -y'
    subprocess.call(command, shell=True)


if __name__ == '__main__':
    pass
    # video_merge_ass()
    # get_part_time()
    # out_set=[]
    # # 测试
    # all_balls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # merge_video(video_result=all_balls)
    # num_balls_to_grab = 5
    # result = grab_balls(all_balls, num_balls_to_grab)
    # print("抓取到的球：", result)

    # # 制作混剪视频
    # video_list=[]
    # for i in range(1,10):
    #     temp = f"C:/Users/83853/Desktop/视频素材/视频素材/轨道交通/2023_050{i}.mp4"
    #     video_list.append(temp)
    # mix(video_list)
    mix(all_balls=['aa.jpg','bb.jpg'],
        video_long_time=6,
        video_min_time=6,
        video_max_time=8,
        video_count=2)

#      图片转视频
