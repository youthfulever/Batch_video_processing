import subprocess

from func_ffprobe import get_ratio


def get_crop_ratio_pic(pic_file, ration_w=1920, ration_h=1080):
    pic_w, pic_h = get_ratio(pic_file)
    if pic_w / pic_h == ration_w / ration_h:
        # print(0)
        command = (
            f'data\\tool\\ffmpeg -i "{pic_file}" -filter_complex "[0:0]scale={ration_w}:{ration_h}" temp/mask.jpg -y'
        )
    elif pic_w / pic_h > ration_w / ration_h:
        # print(1)
        # 居中裁切  竖屏幕
        command = (
            f'data\\tool\\ffmpeg -i "{pic_file}" -filter_complex "[0:0]crop=min(iw\,ih*{ration_w}/{ration_h}):min(ih\,iw*{ration_h}/{ration_w}), scale={ration_w}:{ration_h}" temp/mask.jpg -y'
        )
    elif pic_w / pic_h < ration_w / ration_h:
        # print(2)
        # 居中裁切  heng屏幕
        command = (
            f'data\\tool\\ffmpeg -i "{pic_file}" -filter_complex "[0:0]crop=min(iw\,ih*{ration_w}/{ration_h}):min(ih\,iw*{ration_h}/{ration_w}), scale={ration_w}:{ration_h}" temp/mask.jpg -y'
        )

    subprocess.call(command, shell=True)


def get_crop_ratio_pic_mix(pic_file, out_file, ratio='16/9'):
    if ratio == '16/9':
        ration_w = 1920
        ration_h = 1080
    if ratio == '9/16':
        ration_w = 1080
        ration_h = 1920
    pic_w, pic_h = get_ratio(pic_file)
    if pic_w / pic_h == ration_w / ration_h:
        # print(0)
        command = (
            f'data\\tool\\ffmpeg -i "{pic_file}" -filter_complex "[0:0]scale={ration_w}:{ration_h}" "{out_file}" -y'
        )
    elif pic_w / pic_h > ration_w / ration_h:
        # print(1)
        # 居中裁切  竖屏幕
        command = (
            f'data\\tool\\ffmpeg -i "{pic_file}" -filter_complex "[0:0]crop=min(iw\,ih*{ration_w}/{ration_h}):min(ih\,iw*{ration_h}/{ration_w}), scale={ration_w}:{ration_h}" "{out_file}" -y'
        )
    elif pic_w / pic_h < ration_w / ration_h:
        # print(2)
        # 居中裁切  heng屏幕
        command = (
            f'data\\tool\\ffmpeg -i "{pic_file}" -filter_complex "[0:0]crop=min(iw\,ih*{ration_w}/{ration_h}):min(ih\,iw*{ration_h}/{ration_w}), scale={ration_w}:{ration_h}" "{out_file}" -y'
        )

    subprocess.call(command, shell=True)


# # 居中裁切  竖屏幕
# command = (
#     'ffmpeg -i heng.jpg -filter_complex "[0:0]crop=min(iw\,ih*1080/1920):min(ih\,iw*1920/1080), scale=1080:1920" myout.jpg'
# )
# # 居中裁切  heng屏幕
# command = (
#     'ffmpeg -i shu.jpg -filter_complex "[0:0]crop=min(iw\,ih*1920/1080):min(ih\,iw*1080/1920), scale=1920:1080" output.jpg -y'
# )

if __name__ == '__main__':
    get_crop_ratio_pic(pic_file='temp.jpg', )
