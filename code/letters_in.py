
# import subprocess
# cmd=f'''ffmpeg -i 712.mp4 -vf "drawtext=text='Your Text':fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,1,5)'" temp/output.mp4'''
# subprocess.call(cmd, shell=True)

import subprocess

# cmd = f'''ffmpeg -i 712.mp4 -vf "drawtext=text='Your Text':fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,1,5)'" temp/output.mp4'''
# cmd = f'''ffmpeg -i 712.mp4 -vf "drawtext=text='海阔天空':fontsize=150:fontfile=data/font/my.ttf:fontcolor=red:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,1,5)',fade=in:st=0:d=2, fade=out:st=video_duration-2:d=2[out]" temp/output.mp4 -y'''
# cmd = f'''ffmpeg -i 712.mp4 -vf "[in]drawtext=fontfile=data/font/my.ttf:text='First Line':fontcolor=red:fontsize=40:x=(w-text_w)/2:y=if(lt(t\,3)\,(-h+((3*h-200)*t/6))\,(h-200)/2):enable='between(t,2.9,50)',drawtext=fontfile=data/font/my.ttf: text='Second Line': fontcolor=yellow: fontsize=30: x=if(lt(t\,4)\,(-w+((3*w-tw)*t/8))\,(w-tw)/2): y=(h-100)/2:enable='between(t,3.5,50)',drawtext=fontfile=data/font/my.ttf: text='Third Line': fontcolor=blue: fontsize=50: x=if(lt(t\,5)\,(2*w-((3*w+tw)*t/10))\,(w-tw)/2): y=h/2:enable='between(t,4.5,50)',drawtext=fontfile=data/font/my.ttf: text='Fourth Line': fontcolor=black: fontsize=20: x=(w-text_w)/2: y=if(lt(t\,6)\,(2*h-((3*h-100)*t/12))\,(h+100)/2):enable='between(t,5.5,50)'[out]" temp/output.mp4 -y'''


# # 文字淡入淡出
# cmd='''ffmpeg -i 712.mp4 -lavfi "drawtext=text='Summer Video':fontfile=data/font/my.ttf:fontsize=70:x=w/2:y=h/2:enable='between(t,0,15)':fade=t=in:start_time=0:d=3" -c:a copy temp/output2.mp4'''

#  移动
cmd='''ffmpeg -i 712.mp4 -vf drawtext="fontcolor=red:fontsize=60:fontfile=data/font/my.ttf:line_spacing=7:text=test:x=50+50*t:y=50"  -y out.mp4
'''
subprocess.call(cmd, shell=True)
