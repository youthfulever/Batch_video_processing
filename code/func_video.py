import hashlib
import os
import random
import shutil
import subprocess
import json
import time
from func_os import *
from func_ffprobe import *
from func_pic import get_crop_ratio_pic, get_crop_ratio_pic_mix

# {"none":"","Nvidia":"-c:v h264_cuvid","Intel":"-c:v h264_qsv","AMD":"-hwaccels dxva2"}解码
# {"none":"","Nvidia":"-c:v h264_nvenc","Intel":"-vcodec h264_qsv","AMD":"-c:v h264_amf"}编码
dec = ["-c:v h264_cuvid", "-c:v h264_qsv", "-hwaccels dxva2", ""]
enc = ["-c:v h264_nvenc", "-vcodec h264_qsv", "-c:v h264_amf", "-c:v libx264"]
dec_index = 3
enc_index = 3


def change_gpu(gpu_flag):
    global enc_index
    if gpu_flag == 0:
        enc_index = 3
    if gpu_flag == 1:
        enc_index = 0
    if gpu_flag == 1:
        enc_index = 1


def myedit(input_video, output_video, accurate_cut_flag='0', start_cut_flag='0', start_cut_time='0', end_cut_flag='0',
           end_cut_time='0', end_cut_time_1='0',
           delogo_flag='0', delog_x=0, delog_y=0, delog_w=0, delog_h=0, crop_flag='0', crop_x=0, crop_y=0, crop_w=0,
           crop_h=0, ration_flag='0', ratio_w=1920, ratio_h=1080, padding_color='blue'):
    accurate_cut_dic = {
        '0': '',
        '1': '-accurate_seek',
    }

    # start_cut_time='10'   # 一秒等于1000毫秒
    start_cut_dic = {
        '0': '',
        '1': f'-ss {seconds_to_hhmmss(start_cut_time)}',
    }

    # end_cut_time='10'   # 一秒等于1000毫秒seconds_to_hhmmss((get_video_length(input_video)-float(end_cut_time)))

    end_cut_dic = {
        '0': '',
        '1': f'-to {seconds_to_hhmmss((get_video_length(input_video) - float(end_cut_time)))}',
        '2': f'-to {seconds_to_hhmmss(end_cut_time_1)}',
    }
    # delogo_flag='1'
    # delog_x=200
    # delog_y=300
    # delog_w=20
    # delog_h=20
    delogo_dic = {
        '0': '',
        '1': f'delogo=x={delog_x}:y={delog_y}:w={delog_w}:h={delog_h},'

    }

    # crop_flag='1'
    # crop_x=100
    # crop_y=100
    # crop_w=800
    # crop_h=500
    crop_dic = {
        '0': '',
        '1': f'crop=x={crop_x}:y={crop_y}:w={crop_w}:h={crop_h},'

    }
    ration_dic = {
        '0': '',
        '1': f'scale={ratio_w}:{ratio_h}:force_original_aspect_ratio=decrease,pad={ratio_w}:{ratio_h}:(ow-iw)/2:(oh-ih)/2:{padding_color},'

    }
    filter_complex_dic = {
        '0': '',
        '1': f'-filter_complex "{delogo_dic[delogo_flag]}{crop_dic[crop_flag]}{ration_dic[ration_flag]}"'

    }
    filter_complex_flag = ''
    if crop_flag == '1' or delogo_flag == '1' or ration_flag == '1':
        filter_complex_flag = '1'
    else:
        filter_complex_flag = '0'

    # -vf "drawtext=text='中国':fontfile=data/font/test.ttf:fontsize=23:fontcolor=white:x=200:y=300"
    command = [
        'data\\tool\\ffmpeg',
        dec[dec_index],
        start_cut_dic[start_cut_flag],  # 视频开头时长剪辑
        end_cut_dic[end_cut_flag],  # 视频结尾时间剪辑
        accurate_cut_dic[accurate_cut_flag],  # 是否精准剪辑
        '-i', f'"{input_video}"',  # 输入视频
        filter_complex_dic[filter_complex_flag],  # 去水印+视频裁切
        f'{enc[enc_index]} -c:a aac',
        f'"{output_video}"',  # 输出视频
        '-y'
    ]
    command = [x for x in command if x]  # 删除空元素

    command_str = ' '.join(command)

    subprocess.call(command_str, shell=True)


def remove_duplicate_api(input_file='test.mp4', out_file='newnew.mp4', cut_fps="0", fps='', multi_play_value=1,
                         mate_flag='1',
                         title='', author='', description='', copyright='',
                         cube_flag='0', cube_value='data/lut/01温蓝.cube',
                         gamma='1', brightness='0', contrast='1', saturation='1',
                         mask_flag='0', mask_pic_url='test.jpg', mask_trans='0.5'
                         , type='long'):
    # bug排查，原来只适配30帧的抽帧
    # bug新，抽帧后消除了视频音轨，导致后续报错

    cut_fps = 0 if cut_fps == '' else int(cut_fps)
    frame_rate = int(get_fps(input_file))
    fps = frame_rate - int(cut_fps) if fps == '' else int(fps)

    if type == 'temp':
        command = f'data\\tool\\ffmpeg -i "{input_file}" -to 00:00:05 temp/temp.mp4 -y'
        subprocess.call(command, shell=True)
        input_file = 'temp/temp.mp4'
    if int(cut_fps) > 0:
        folder_path = 'temp/fps'
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
        command = f'data\\tool\\ffmpeg -i "{input_file}"  temp/fps/%d.jpg'
        subprocess.call(command, shell=True)
        for file in sorted(os.listdir(folder_path), key=lambda x: int(x[:-4])):
            base_name, end = os.path.splitext(file)
            if int(base_name) % frame_rate <=(frame_rate-cut_fps) and int(base_name) % frame_rate >=1:

                file_path = f'{folder_path}/{file}'
                new_base_name =  int(int(base_name) / frame_rate)*(frame_rate-cut_fps)+int(base_name) % frame_rate
                new_file_path = f'{folder_path}/{new_base_name}{end}'
                # print(file_path,new_file_path)
                shutil.move(file_path, new_file_path)
            else:
                file_path = f'{folder_path}/{file}'
                os.remove(file_path)

            # if int(base_name) % frame_rate == 0:
            #     continue
            # file_path = f'{folder_path}/{file}'
            # new_base_name = int(base_name) - int(int(base_name) / frame_rate)
            # new_file_path = f'{folder_path}/{new_base_name}{end}'
            # shutil.move(file_path, new_file_path)
        command = f'data\\tool\\ffmpeg -framerate {frame_rate - int(cut_fps)} -i temp/fps/%d.jpg  {enc[enc_index]} -pix_fmt yuv420p temp/tempfps.mp4 -y'
        # print(command)
        subprocess.call(command, shell=True)
        command = f'data\\tool\\ffmpeg -i temp/tempfps.mp4 -i "{input_file}" -map 0:v -map 1:a -c:v libx264 -c:a aac -shortest temp/tempA.mp4 -y'  # TODO
        subprocess.call(command, shell=True)
        input_file = 'temp/tempA.mp4'

    cube_dic = {
        '0': '',
        '1': f'lut3d={cube_value},'

    }
    time_md5 = hashlib.md5(str(time.time()).encode()).hexdigest()
    if title == '':
        title = time_md5
    if author == '':
        author = time_md5
    if description == '':
        description = time_md5
    if copyright == '':
        copyright = time_md5

    meta_str_dic = {
        '0': '',
        '1': f'-metadata title="{title}" -metadata author="{author}" -metadata description="{description}" -metadata copyright="{copyright}"'

    }

    if mask_flag == '1':
        ration_w, ratio_h = get_ratio(input_file)
        get_crop_ratio_pic(mask_pic_url, ration_w, ratio_h)
        mask_pic_url = 'temp/mask.jpg'
    if mask_flag == '1':
        command = [
            'data\\tool\\ffmpeg',
            dec[dec_index],
            '-i', f'"{input_file}"',  # 输入视频
            f'-i "{mask_pic_url}"',
            f'-filter_complex "[1]format=rgba,colorchannelmixer=aa={mask_trans}[alpha];[0:v]fps={fps},setpts=PTS/{multi_play_value},{cube_dic[cube_flag]}eq=gamma={gamma}:brightness={brightness}:contrast={contrast}:saturation={saturation}[temp];[temp][alpha]overlay" '
            f'-af "atempo={multi_play_value}"',  # 默认有倍速，实在不行设为1
            meta_str_dic[mate_flag],
            f'{enc[enc_index]} -c:a aac',
            f'"{out_file}"',  # 输出视频
            '-y'
        ]
    if mask_flag == '0':
        command = [
            'data\\tool\\ffmpeg',
            dec[dec_index],
            '-i',f'"{input_file}"',  # 输入视频
            f'-filter_complex "[0:v]fps={fps},setpts=PTS/{multi_play_value},{cube_dic[cube_flag]}eq=gamma={gamma}:brightness={brightness}:contrast={contrast}:saturation={saturation}" '
            f'-af "atempo={multi_play_value}"',  # 默认有倍速，实在不行设为1
            meta_str_dic[mate_flag],
            f'{enc[enc_index]} -c:a aac',
            f'"{out_file}"',  # 输出视频
            '-y'
        ]
    command = [x for x in command if x]  # 删除空元素
    command_str = ' '.join(command)
    # print(command_str)
    subprocess.call(command_str, shell=True)


def ending_api(input_file='712.mp4', out_file='newnew.mp4', extension='.mp4', ratio_h='1920', ratio_w='1080',
               ration_flag="2", padding_color='white',
               blur_level='8', audio_able='0', bg_audio_flag='1', bg_audio_file='38s.mp3', bg_audio_volume='1',
               title_start='', title_end='', video_start_file='', video_end_file='', padding_pic='heng.jpg',
               quality='23', quality_flag='1', ass_list=[], ass_type_list=[], ass_time_list=[]

               ):  # blur_level设置为1-10比较合适 推荐6
    out_file = get_new_extension(out_file, extension)
    if title_start != '' or title_end != '':
        foldername, filename = get_file_part(out_file)
        out_file = foldername + '/' + title_start + filename + title_end + extension
    # print(title_start,title_end)
    radius = int(blur_level) * 2
    variance = blur_level
    bg_audio_dic = {
        '0': '',
        '1': f'-i "{bg_audio_file}"'

    }
    # bg_audio_flag
    # '不添加背景音乐':0
    # '添加背景音乐':1
    audie_dic = {
        '0': f';[0:a]volume={audio_able}[end_a]',
        '1': f';[0:a]volume={audio_able}[a1];[1:a]volume={bg_audio_volume}[a2];[a1][a2]amix=inputs=2:duration=first[end_a]'

    }
    pic_padding_flag = '1' if ration_flag == '4' else '0'
    pic_padding_dic = {
        '0': '',
        '1': f'-i "{padding_pic}"'
    }

    # 因为要考虑音频和视频的相互影响
    # 现在情况是一定有图片不一定有音频
    # 01 横屏
    # 情况0 1音频+2图片 (有音频)
    # 情况1 1图片（无音频)

    if bg_audio_flag == '1' and int(ratio_h) > int(ratio_w):  # 竖屏
        audio_pic_padding_flag = '2'
    if bg_audio_flag == '1' and int(ratio_h) <= int(ratio_w):  # 竖屏
        audio_pic_padding_flag = '0'

    if bg_audio_flag == '0' and int(ratio_h) > int(ratio_w):  # 竖屏
        audio_pic_padding_flag = '3'
    if bg_audio_flag == '0' and int(ratio_h) <= int(ratio_w):  # 竖屏
        audio_pic_padding_flag = '1'

    audio_pic_padding_dic = {
        #  01 横屏
        '0': f'[0:a]volume={audio_able}[a1];[1:a]volume={bg_audio_volume}[a2];[a1][a2]amix=inputs=2:duration=first[end_a];[0:v]scale={ratio_h}*iw/ih:{ratio_h}[tempv];[2:0]crop=min(iw\,ih*{ratio_w}/{ratio_h}):min(ih\,iw*{ratio_h}/{ratio_w}), scale={ratio_w}:{ratio_h}[pic];[pic][tempv]overlay=(W-w)/2:0,setsar=1[end_v]',
        '1': f'[0:a]volume={audio_able}[end_a];[0:v]scale={ratio_h}*iw/ih:{ratio_h}[tempv];[1:0]crop=min(iw\,ih*{ratio_w}/{ratio_h}):min(ih\,iw*{ratio_h}/{ratio_w}), scale={ratio_w}:{ratio_h}[pic];[pic][tempv]overlay=(W-w)/2:0,setsar=1[end_v]',
        #  23 竖屏
        '2': f'[0:a]volume={audio_able}[a1];[1:a]volume={bg_audio_volume}[a2];[a1][a2]amix=inputs=2:duration=first[end_a];[0:v]scale={ratio_w}:ih*{ratio_w}/iw[tempv];[2:0]crop=min(iw\,ih*{ratio_w}/{ratio_h}):min(ih\,iw*{ratio_h}/{ratio_w}), scale={ratio_w}:{ratio_h}[pic];[pic][tempv]overlay=0:(H-h)/2,setsar=1[end_v]',
        '3': f'[0:a]volume={audio_able}[end_a];[0:v]scale={ratio_w}:ih*{ratio_w}/iw[tempv];[1:0]crop=min(iw\,ih*{ratio_w}/{ratio_h}):min(ih\,iw*{ratio_h}/{ratio_w}), scale={ratio_w}:{ratio_h}[pic];[pic][tempv]overlay=0:(H-h)/2,setsar=1[end_v]'

    }
    # 0 不改变尺寸
    # 1 改变尺寸  颜色填充
    # 23 改变尺寸 模糊延拓
    # 4 改变尺寸 图片填充

    ration_dic = {
        '0': f'-filter_complex "[0:v]setpts=1*PTS,setsar=1[end_v]{audie_dic[bg_audio_flag]}" -map "[end_v]" -map "[end_a]" ',
        '1': f'-filter_complex "[0:v]scale={ratio_w}:{ratio_h}:force_original_aspect_ratio=decrease,pad={ratio_w}:{ratio_h}:(ow-iw)/2:(oh-ih)/2:{padding_color},setsar=1[end_v]{audie_dic[bg_audio_flag]}" -map "[end_v]" -map "[end_a]" ',
        '2': f'-filter_complex "[0:v]split[a][b];[a]scale={ratio_w}:{ratio_h},boxblur={radius}:{variance}[1];[b]scale={ratio_h}*iw/ih:{ratio_h}[2];[1][2]overlay=(W-w)/2:0,setsar=1[end_v]{audie_dic[bg_audio_flag]}" -map "[end_v]" -map "[end_a]" -aspect {ratio_w}:{ratio_h} ',
        # 输出 1920:1080  or 1080:720
        '3': f'-filter_complex "[0:v]split[a][b];[a]scale={ratio_w}:{ratio_h},boxblur={radius}:{variance}[1];[b]scale={ratio_w}:ih*{ratio_w}/iw[2];[1][2]overlay=0:(H-h)/2,setsar=1[end_v]{audie_dic[bg_audio_flag]}" -map "[end_v]" -map "[end_a]" -aspect {ratio_w}:{ratio_h} ',
        # 输出1080:1920  or 720:1080
        '4': f'-filter_complex "{audio_pic_padding_dic[audio_pic_padding_flag]}" -map "[end_v]" -map "[end_a]" ',

    }

    command = [
        'data\\tool\\ffmpeg',
        dec[dec_index],
        '-i',f'"{input_file}"',  # 输入视频
        bg_audio_dic[bg_audio_flag],
        pic_padding_dic[pic_padding_flag],
        ration_dic[ration_flag],
        f'{enc[enc_index]} -c:a aac ',
        'temp/temp.mp4',  # 输出视频
        '-y'
    ]

    command = [x for x in command if x]  # 删除空元素
    command_str = ' '.join(command)
    # print(command_str)
    subprocess.call(command_str, shell=True)

    start_flag = 'start' if video_start_file != '' else '0'
    end_flag = 'end' if video_end_file != '' else '0'
    if start_flag == 'start' and end_flag == '0':
        filter_flag = '0'
    elif start_flag == '0' and end_flag == 'end':
        filter_flag = '1'
    elif start_flag == 'start' and end_flag == 'end':
        filter_flag = '2'

    if video_start_file != '' or video_end_file != '':
        ratio_w, ratio_h = get_ratio('temp/temp.mp4')
        #  0只加片头 1只加片尾 2片头片尾都加
        filter_complex_dic = {
            '0': f'-filter_complex "[0:v]scale={ratio_w}:{ratio_h}:force_original_aspect_ratio=decrease,pad={ratio_w}:{ratio_h}:(ow-iw)/2:(oh-ih)/2,setsar=1[new0v];[new0v][0:a][1:v][1:a]concat=n=2:v=1:a=1" ',
            '1': f'-filter_complex "[1:v]scale={ratio_w}:{ratio_h}:force_original_aspect_ratio=decrease,pad={ratio_w}:{ratio_h}:(ow-iw)/2:(oh-ih)/2,setsar=1[new1v];[0:v][0:a][new1v][1:a]concat=n=2:v=1:a=1" ',
            '2': f'-filter_complex "[0:v]scale={ratio_w}:{ratio_h}:force_original_aspect_ratio=decrease,pad={ratio_w}:{ratio_h}:(ow-iw)/2:(oh-ih)/2,setsar=1[new0v];[2:v]scale={ratio_w}:{ratio_h}:force_original_aspect_ratio=decrease,pad={ratio_w}:{ratio_h}:(ow-iw)/2:(oh-ih)/2,setsar=1[new2v];[new0v][0:a][1:v][1:a][new2v][2:a]concat=n=3:v=1:a=1" ',
        }

        input_dic = {
            '0': '',
            'start': f'-i "{video_start_file}" ',
            'end': f'-i "{video_end_file}" '
        }
        quality_dic = {
            '0': '-vsync cfr ',
            '1': f'-vsync cfr -crf {quality} ',

        }
        command = [
            'data\\tool\\ffmpeg',
            input_dic[start_flag],
            dec[dec_index],
            '-i', 'temp/temp.mp4',  # 输入视频
            input_dic[end_flag],
            filter_complex_dic[filter_flag],
            f'{enc[enc_index]} -c:a aac',
            quality_dic[quality_flag],
            'temp/temp_ass.mp4',  # 输出视频
            '-y'
        ]
        command = [x for x in command if x]  # 删除空元素
        command_str = ' '.join(command)
        # print(command_str)
        subprocess.call(command_str, shell=True)
    else:
        move_file('temp/temp.mp4', 'temp/temp_ass.mp4')

    temp_long_time = get_video_length('temp/temp_ass.mp4')
    # print(ass_time_list)
    for i in range(len(ass_list)):
        if ass_time_list[i]['end'] != '':
            time_end = ass_time_list[i]['end']
        else:
            time_end = temp_long_time
        time_end = seconds_to_hhmmss(time_end)

        if ass_time_list[i]['start'] != '':
            time_start = ass_time_list[i]['start']
        else:
            time_start = 0

        if ass_type_list[i] != '动态浮现':
            time_start1 = time_start
            time_start2 = 0
        if ass_type_list[i] == '动态浮现':
            time_start1 = float(time_start) + 0.5
            time_start2 = float(time_start) + 1
        time_start1 = seconds_to_hhmmss(time_start1)
        time_start2 = seconds_to_hhmmss(time_start2)

        change_ass_longtime(output_file_path=ass_list[i], long_time=time_end, time_start1=time_start1,
                            time_start2=time_start2)
    # change_ass_longtime(output_file_path,long_time,time_start1,time_start2):
    video_merge_ass(video='temp/temp_ass.mp4', ass_list=ass_list, out_video=out_file)


def cut_change_fps(input_file='test.mp4', cut_fps=1):
    folder_path = 'temp/fps'
    shutil.rmtree(folder_path)
    os.makedirs(folder_path)
    frame_rate = int(get_fps(input_file))
    command = f'data\\tool\\ffmpeg -i test.mp4  temp/fps/%d.jpg'
    subprocess.call(command, shell=True)
    for file in sorted(os.listdir(folder_path), key=lambda x: int(x[:-4])):
        base_name, end = os.path.splitext(file)
        if int(base_name) % frame_rate == 0:
            continue
        file_path = f'{folder_path}/{file}'
        new_base_name = int(base_name) - int(int(base_name) / 30)
        new_file_path = f'{folder_path}/{new_base_name}{end}'
        shutil.move(file_path, new_file_path)
    command = f'data\\tool\\ffmpeg -framerate {frame_rate - cut_fps} -i temp/fps/%d.jpg  -vf fps=26 {enc[enc_index]} -pix_fmt yuv420p newnew.mp4 -y'
    subprocess.call(command, shell=True)


def water_api(input_file='712.mp4', out_file='newnew.mp4',
              text_flag='1', text='hello', font_size=0.5, text_time_flag='1', text_time='3', text_x='0.2', text_y='0.2',
              pic_flag='0', pic_file='heng.jpg', pic_size_w='0.1', pic_time_flag='1', pic_time='3', pic_x='0',
              pic_y='0.5',
              gif_flag='0', gif_file='test.gif', gif_size_w='0.5', gif_time_flag='1', gif_time='3', gif_x='0.5',
              gif_y='0.5',
              ):
    # 字体大小是像素大小
    ratio_w, ratio_h = get_ratio(input_file)
    text_x = float(text_x) * ratio_w
    text_y = float(text_y) * ratio_h
    pic_x = float(pic_x) * ratio_w
    pic_y = float(pic_y) * ratio_h
    gif_x = float(gif_x) * ratio_w
    gif_y = float(gif_y) * ratio_h
    # 调节时间 0全部时间 1开始几秒 （0，time） 2结束几秒 （long_time-time,long_time）
    video_long_time = get_video_length(input_file)
    pic_size_w = float(pic_size_w) * ratio_w
    gif_size_w = float(gif_size_w) * ratio_w

    def get_time(time_flag, time):
        if time_flag == '0':
            start_time = 0
            end_time = video_long_time
        if time_flag == '1':
            start_time = 0
            end_time = time
        if time_flag == '2':
            start_time = video_long_time - float(time)
            end_time = video_long_time
        return start_time, end_time

    text_start_time, text_end_time = get_time(text_time_flag, text_time)
    pic_start_time, pic_end_time = get_time(pic_time_flag, pic_time)
    gif_start_time, gif_end_time = get_time(gif_time_flag, gif_time)

    font_size = font_size * ratio_h
    pic_in_dic = {
        '0': '',
        '1': f'  -i "{pic_file}"'
    }
    gif_in_dic = {
        '0': '',
        '1': f' -ignore_loop 0 -i "{gif_file}"'
    }
    # 文字 图片 gif
    # 0 只有文字
    filter_complex_flag = text_flag + pic_flag + gif_flag
    filter_complex_dic = {
        # 单个
        '100': f'''-filter_complex "[0:v]drawtext=text={text}:fontfile=data/font/my.ttf:fontsize={font_size}:fontcolor=white:x={text_x}:y={text_y}:enable='between(t,{text_start_time},{text_end_time})'" ''',
        '010': f'''-filter_complex "[1:v]scale={pic_size_w}:-1[pic];[0:v][pic]overlay={pic_x}:{pic_y}:enable='between(t,{pic_start_time},{pic_end_time})'" ''',
        '001': f'''-filter_complex "[1:v]scale={gif_size_w}:-1[pic];[0:v][pic]overlay={gif_x}:{gif_y}:enable='between(t,{gif_start_time},{gif_end_time})'" -shortest ''',
        # 两个
        '101': f'''-filter_complex "[0:v]drawtext=text={text}:fontfile=data/font/my.ttf:fontsize={font_size}:fontcolor=white:x={text_x}:y={text_y}:enable='between(t,{text_start_time},{text_end_time})'[text];[1:v]scale={gif_size_w}:-1[pic];[text][pic]overlay={gif_x}:{gif_y}:enable='between(t,{gif_start_time},{gif_end_time})'" -shortest ''',
        '110': f'''-filter_complex "[0:v]drawtext=text={text}:fontfile=data/font/my.ttf:fontsize={font_size}:fontcolor=white:x={text_x}:y={text_y}:enable='between(t,{text_start_time},{text_end_time})'[text];[1:v]scale={pic_size_w}:-1[pic];[text][pic]overlay={pic_x}:{pic_y}:enable='between(t,{pic_start_time},{pic_end_time})'" ''',
        '000': f'''-filter_complex "[0:v]drawtext=text=' ':fontfile=data/font/my.ttf:fontsize={font_size}:fontcolor=white:x={text_x}:y={text_y}:enable='between(t,{text_start_time},{text_end_time})'" ''',

        '111': f'''-filter_complex "[0:v]drawtext=text={text}:fontfile=data/font/my.ttf:fontsize={font_size}:fontcolor=white:x={text_x}:y={text_y}:enable='between(t,{text_start_time},{text_end_time})'[text];[1:v]scale={pic_size_w}:-1[pic];[text][pic]overlay={pic_x}:{pic_y}:enable='between(t,{pic_start_time},{pic_end_time})'[temp];[2:v]scale={gif_size_w}:-1[gif];[temp][gif]overlay={gif_x}:{gif_y}:enable='between(t,{gif_start_time},{gif_end_time})'" -shortest ''',
        '011': f'''[1:v]scale={pic_size_w}:-1[pic];[0:v][pic]overlay={pic_x}:{pic_y}:enable='between(t,{pic_start_time},{pic_end_time})'[temp];[2:v]scale={gif_size_w}:-1[gif];[temp][gif]overlay={gif_x}:{gif_y}:enable='between(t,{gif_start_time},{gif_end_time})'" -shortest ''',

    }
    #  添加gif命令 ffmpeg  -i 712.mp4 -ignore_loop 0 -i test.gif -filter_complex "[0:v][1:v]overlay=10:10:enable='between(t,0,10)'" -shortest out.mp4 -y
    command = [
        'data\\tool\\ffmpeg',
        dec[dec_index],
        '-i',f'"{input_file}"',  # 输入视频
        pic_in_dic[pic_flag],
        gif_in_dic[gif_flag],
        filter_complex_dic[filter_complex_flag],
        # f'''-filter_complex "[0:v]drawtext=text=' ':fontfile=data/font/my.ttf:fontsize={font_size}:fontcolor=white:x={text_x}:y={text_y}:enable='between(t,{text_start_time},{text_end_time})'" '''
        # f'''-filter_complex "[1:v]scale={pic_size_w}:-1[pic];[0:v][pic]overlay=10:10:enable='between(t,2,6)'" '''
        # f'''-filter_complex "[0:v][1:v]overlay=10:10:enable='between(t,0,0)'" -shortest '''
        # f'''-filter_complex "[0:v][1:v]overlay=10:10" -shortest '''
        f'{enc[enc_index]} -c:a aac ',
        f'"{out_file}"',  # 输出视频
        '-y'
    ]
    command = [x for x in command if x]  # 删除空元素

    command_str = ' '.join(command)
    # print(filter_complex_flag)
    # print(command_str)
    subprocess.call(command_str, shell=True)


def remove_duplicate(input_video, output_video, fps_flag='1', fps_value=29, multi_play_value=1,
                     title='', author='', description='', copyright=''):
    # fps_flag = '1'
    # fps_value=28
    fps_dic = {
        '0': '',
        '1': f'-vf fps={fps_value}'

    }

    # multi_play_value = 2

    cube_flag = '1'
    cube_value = 'data/lut/01温蓝.cube'
    cube_dic = {
        '0': '',
        '1': f'lut3d={cube_value},'

    }
    # 修改视频元数据
    # ffmpeg - i
    # input.mp4
    # - metadata title = "New Title"
    # - metadata author = "New Author"
    # - metadata description = "New Description"
    # - metadata copyright = "New Copyright"
    # output.mp4

    time_md5 = hashlib.md5(str(time.time()).encode()).hexdigest()
    if title == '':
        title = time_md5
    if author == '':
        author = time_md5
    if description == '':
        description = time_md5
    if copyright == '':
        copyright = time_md5
    metadata_str = f'-metadata title="{title}" -metadata author="{author}" -metadata description="{description}" -metadata copyright="{copyright}"'

    command = [
        'data\\tool\\ffmpeg',
        dec[dec_index],
        '-i',f'"{input_video}"',  # 输入视频
        fps_dic[fps_flag],
        f'-vf "setpts=PTS/{multi_play_value},{cube_dic[cube_flag]}" -af "atempo={multi_play_value}"',  # 默认有倍速，实在不行设为1

        metadata_str,
        f'{enc[enc_index]} -c:a aac ',
        f'"{output_video}"',  # 输出视频
        '-y'
    ]
    command = [x for x in command if x]  # 删除空元素

    command_str = ' '.join(command)
    # print(command_str)
    subprocess.call(command_str, shell=True)


# def mix_video_api():
#     pass

def mix_video_api(all_balls,
                  video_long_time=9,
                  video_min_time=3,
                  video_max_time=4,
                  pic_ratio="16/9", out_count=2, audio_able='0', ratio_w=1920, ratio_h=1080, transitions_value='0',
                  ):
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

    def mix(all_balls=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            video_long_time=10,
            video_min_time=5,
            video_max_time=6, pic_ratio='16/9', out_count=10, audio_able='0', ratio_w=1920, ratio_h=1080,
            transitions_value='0'
            ):
        for i in range(out_count):
            temp_balls = all_balls.copy()
            time_list = get_part_time(video_long_time=video_long_time, video_min_time=video_min_time,
                                      video_max_time=video_max_time)

            video_result = grab_balls(temp_balls, len(time_list))
            start_end_list = get_start_end_time(time_list, video_result)
            # print(start_end_list, video_result)
            merge_video(start_end_list, video_result, pic_ratio=pic_ratio, audio_able=audio_able, ratio_w=ratio_w,
                        ratio_h=ratio_h, transitions_value=transitions_value)
            print(f"混剪——第{i}个完成！")

    def get_start_end_time(time_list, video_result):
        start_end_list = []
        for i in range(len(time_list)):
            _, file_extension = os.path.splitext(video_result[i])
            temp_dic = {
                'start': '',
                'end': '',
            }
            if file_extension != '.jpg':
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
            if file_extension == '.jpg':
                temp_dic['start'] = 0
                temp_dic['end'] = time_list[i]
                start_end_list.append(temp_dic)

        return start_end_list

    def merge_video(start_end_list, video_result=[], ratio_w=1080, ratio_h=1920, audio_able='0', transitions_flag='1',
                    transitions_value='0', pic_ratio='16/9'):

        for i in range(len(video_result)):
            _, file_extension = os.path.splitext(video_result[i])
            if file_extension == '.jpg':
                file_name = os.path.basename(video_result[i])
                pic_name = 'temp/' + file_name
                file_name = get_new_extension(pic_name, '.mp4')
                mp4_name = get_unique_filename(file_name)
                get_crop_ratio_pic_mix(pic_file=video_result[i], out_file=pic_name, ratio='16/9')
                if pic_ratio == '16/9':
                    pic_ration_w = 1920
                    pic_ration_h = 1080
                if pic_ratio == '9/16':
                    pic_ration_w = 1080
                    pic_ration_h = 1920
                filter_complex = f''' -filter_complex "[0:0]scale=8000:-1,zoompan=z='zoom+0.001':x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d=6*60:s={pic_ration_w}x{pic_ration_h}:fps=60" '''
                command = f'data\\tool\\ffmpeg -loop 1 -framerate 60 -i "{pic_name}" -f lavfi -i anullsrc=r=48000:cl=stereo {filter_complex} -c:v libx264 -c:a aac -shortest -t {start_end_list[i]["end"] + 0.5} {mp4_name} -y'
                # print(command)
                subprocess.call(command, shell=True)

                video_result[i] = mp4_name

        in_str = ''
        scale_str = ''
        merge_str = ''
        transitions_value = float(transitions_value) / 2

        for i in range(len(video_result)):
            transitions_dic = {
                '0': '',
                '1': f',fade=in:st=0:d={transitions_value},fade=out:st={start_end_list[i]["end"] - start_end_list[i]["start"] - transitions_value}:d={transitions_value}'
            }
            in_str += f' -i "{video_result[i]}" '
            scale_str += f'[{i}:v]scale={ratio_w}:{ratio_h}:force_original_aspect_ratio=decrease,pad={ratio_w}:{ratio_h}:(ow-iw)/2:(oh-ih)/2,setsar=1,trim=start={start_end_list[i]["start"]}:end={start_end_list[i]["end"]},setpts=PTS-STARTPTS{transitions_dic[transitions_flag]},setsar=1[new{i}v];[{i}:a]atrim=start={start_end_list[i]["start"]}:end={start_end_list[i]["end"]},asetpts=PTS-STARTPTS[new{i}a];'
            merge_str += f'[new{i}v][new{i}a]'
        filter_complex_str = f'-filter_complex "{scale_str}{merge_str}concat=n={len(video_result)}:v=1:a=1[outv][outa];[outa]volume={audio_able}[outa];[outv]fps=30[outv]"'
        # filter_complex_str = f'-filter_complex "{scale_str}{merge_str}concat=n={len(video_result)}:v=1:a=1"'
        command = [
            'data\\tool\\ffmpeg',
            in_str,
            filter_complex_str,
            # f'temp/{str(time.time())[-5:]}.mp4',  # 输出视频
            ' -vsync 2 -map "[outv]" -map "[outa]" ',
            # f'{enc[enc_index]} -c:a aac',
            f'out/混剪_{str(time.time())[0:10]}.mp4',  # 输出视频
            '-y'
        ]

        command = [x for x in command if x]  # 删除空元素
        command_str = ' '.join(command)
        # print(command_str)
        subprocess.call(command_str, shell=True)

    mix(all_balls, video_long_time, video_min_time, video_max_time, pic_ratio=pic_ratio, out_count=out_count,
        audio_able=audio_able, ratio_w=ratio_w, ratio_h=ratio_h, transitions_value=transitions_value)


def video_merge_ass(video='712.mp4', ass_list=['data/ass/temp1.ass', 'data/ass/temp2.ass'], out_video='temp/temp.mp4'):
    ass_str = ''
    if len(ass_list) == 0:
        command = f'data\\tool\\ffmpeg -i "{video}"  "{out_video}" -y'
    else:
        for i in ass_list:
            ass_str += f'subtitles={i},'
        command = f'data\\tool\\ffmpeg -i "{video}" -vf "{ass_str}" "{out_video}" -y'
    # print(command)
    subprocess.call(command, shell=True)


def videotogif(input_file='test.mp4', output_file='test.gif', gif_ss='0', gif_to='3'):
    gif_ss = seconds_to_hhmmss(gif_ss)
    gif_to = seconds_to_hhmmss(gif_to)
    command = f'data\\tool\\ffmpeg -ss "{gif_ss}" -to "{gif_to}" -i "{input_file}" \
    -vf "fps=10,scale=500:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
    -loop 0 "{output_file}" -y'
    subprocess.call(command, shell=True)

def videotomp3(input_file='logo.mp4', output_file='temp.mp3'):
    command = f'data\\tool\\ffmpeg -i "{input_file}" -q:a 0 -map a "{output_file}" -y'
    subprocess.call(command, shell=True)



if __name__ == '__main__':
    # pass
    videotomp3()
    # video_merge_ass(ass_list=[])
    # mix_video_api(['712.mp4', 'logo.mp4', 'b.mp4'])
    # input_video = 'logo.mp4'
    # output_video = 'out.mp4'
    # water_api(text_x=0.00142857,text_y=0.852791878,font_size=0.14467)
    # myedit(input_video='logo.mp4',output_video='out.mp4',accurate_cut_flag='1',
    #        start_cut_flag='1',start_cut_time='0',end_cut_flag='2',end_cut_time='10',end_cut_time_1='10',
    #         delogo_flag='0',delog_x='200',delog_y='300',delog_w='20.517454545',delog_h='20.348',
    #        crop_flag='0',crop_x='100',crop_y='100',crop_w='800',crop_h='500',
    #        ration_flag='1',ratio_w='400',ratio_h='1280',padding_color='white')
    # remove_duplicate(input_video,output_video)

    # remove_duplicate_api(fps="28",mask_flag='0',type='temp')
    # remove_duplicate_api(out_file='temp/pre.mp4',cut_fps='', fps='', multi_play_value='1', mate_flag='0', title='', author='', description='',
    #                      copyright='', cube_flag='0', cube_value='data/lut/01温蓝.cube', gamma='1', brightness='0',
    #                      contrast='1', saturation='1', mask_flag='1', mask_pic_url='test.jpg', mask_trans='0.5',type='temp')
