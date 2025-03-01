import os
import shutil
from func_ffprobe import seconds_to_hhmmss

# 得到所有视频文件
def find_video_files(folder_path):

    def is_video_file(file_path):
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.mpeg']
        file_extension = os.path.splitext(file_path)[1].lower()
        return file_extension in video_extensions

    video_files = []
    for file in os.listdir(folder_path):
        if is_video_file(file):
                video_files.append(folder_path+'/'+file)
    return video_files

def find_cube_files(folder_path):

    def is_cube_file(file_path):
        cube_extensions = '.cube'
        file_extension = os.path.splitext(file_path)[1].lower()
        return file_extension == cube_extensions

    cube_files = []
    for file in os.listdir(folder_path):
        if is_cube_file(file):
                cube_files.append(file)
    return cube_files

def get_unique_filename(filename):
    new_filename=filename
    base_name, extension = os.path.splitext(filename)
    counter = 1

    while os.path.exists(filename):
        new_filename = f"{base_name}_{counter}{extension}"
        counter += 1
        break
    return new_filename

def get_new_extension(filename,new_extension):
    base_name, extension = os.path.splitext(filename)
    return base_name+new_extension
def get_file_part(filename):
    foldername = os.path.dirname(filename)
    filename = os.path.splitext(os.path.basename(filename))[0]
    return foldername,filename

def move_file(original_file,target_path):
    shutil.move(original_file, target_path)

# def copy_file(original_file,target_path):
#     shutil.copy(original_file, target_path)

def save_ass(ass_content,output_file_path):
    # 将内容写入文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(ass_content)

def change_ass_longtime(output_file_path,long_time,time_start1='',time_start2=''):
    try:
        with open(output_file_path, 'r', encoding='utf-8') as infile:
            content = infile.read()

            # 在这里执行你的字符串替换操作
            # 假设my_time和new_time是你要替换的实际字符串，注意转义字符问题
            content = content.replace('time_not_defined', long_time)
            content = content.replace('time_start1_not_defined',time_start1)
            content = content.replace('time_start2_not_defined',time_start2)

        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(content)

    except FileNotFoundError:
        print("文件未找到")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == '__main__':
    # pass
    # copy_file('data/conf/temp.toml','data/conf/conf5.toml')
    print(get_new_extension('./data/lut/test.mp4','.flv'))
    # print(get_unique_filename("temp/mask.jpg"))