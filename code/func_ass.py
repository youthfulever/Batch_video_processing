from func_ffprobe import seconds_to_hhmmss


def get_ass(text='海阔天空', font_name='华文新魏', font_size=80, font_color='#7fff00', long_time=5, ass_type='动态浮现',
            posx=856, posy=548,ratio_w=1920,ratio_h=1080,start_time1=0.5,start_time2=1):
    font_color=hex_to_ass_color(font_color)
    if long_time!='time_not_defined':
        long_time = seconds_to_hhmmss(long_time)
    if start_time1!='time_start1_not_defined':
        if  ass_type!='动态浮现':
            start_time1=0
        start_time1 = seconds_to_hhmmss(start_time1)
    if start_time2!='time_start2_not_defined':
        start_time2 = seconds_to_hhmmss(start_time2)
    if ass_type == '无效果':
        dila_str = f'Dialogue: 0,{start_time1},{long_time},样式1,,0,0,0,,{{\pos({posx},{posy})}}{text}'
        # print(dila_str)
    if ass_type == '动态浮现':
        dila_str = f'''Dialogue: 1,{start_time1},{start_time2},样式1,,0,0,0,,{{\pos({posx},{posy})\clip(555,1017,625,1017)\\t(0,500,\clip(555,1007,625,1017))\\blur2}}{text}
Dialogue: 1,{start_time1},{start_time2},样式1,,0,0,0,,{{\pos({posx},{posy})\clip(555,1027,625,1027)\\t(0,500,\clip(555,1017,625,1027))\\blur2}}{text}
Dialogue: 1,{start_time1},{start_time2},样式1,,0,0,0,,{{\pos({posx},{posy})\clip(555,1037,625,1037)\\t(0,500,\clip(555,1027,625,1037))\\blur2}}{text}
Dialogue: 1,{start_time1},{start_time2},样式1,,0,0,0,,{{\pos({posx},{posy})\clip(555,1047,625,1047)\\t(0,500,\clip(555,1037,625,1047))\\blur2}}{text}
Dialogue: 1,{start_time1},{start_time2},样式1,,0,0,0,,{{\pos({posx},{posy})\clip(555,1057,625,1057)\\t(0,500,\clip(555,1047,625,1057))\\blur2}}{text}
Dialogue: 1,{start_time1},{start_time2},样式1,,0,0,0,,{{\pos({posx},{posy})\clip(555,1067,625,1067)\\t(0,500,\clip(555,1057,625,1067))\\blur2}}{text}
Dialogue: 0,{start_time2},{long_time},样式1,,0,0,0,,{{\pos({posx},{posy})\\t(0,300,\\bord5\\blur3)\\t(300,800,\\bord2\\blur1)}}{text}
        '''
        # print(dila_str)
    if ass_type == '拉伸闪入':
        text_count= len(text)
        start_posx=posx-text_count*font_size/2+font_size/2
        dila_str=''
        for i in range(text_count):
            dila_str+=f'''Dialogue: 0,{start_time1},{long_time},样式1,,0,0,0,fx,{{\pos({start_posx+font_size*i},{posy})\\an5\\alpha&ff&\\fscx1356\\be10\\blur10\\bord0\\3c&H444444&\\t(140,418,\\alpha&0&\\fscx100\\blur0\\be0)}}{text[i]}
'''
        # print(dila_str)
    if ass_type == '淡入淡出':
        dila_str = f'Dialogue: 0,{start_time1},{long_time},样式1,,0,0,0,,{{\pos({posx},{posy})\\fad(500,0)}}{text}'
        # print(dila_str)
    if ass_type == '移动划入':
        dila_str = f'''Dialogue: 0,{start_time1},{long_time},样式1,,0,0,0,,{{\\fad(500,0)\move({posx+20},{posy},{posx},{posy},0,300)}}{text}
        '''
        # print(dila_str)
    if ass_type == '由大变小':
        dila_str = f'''Dialogue: 0,{start_time1},{long_time},样式1,,0,0,0,,{{\pos({posx},{posy})\\t(0,250,\\fs{font_size+15})\\t(250,500,\\fs{font_size+10})\\t(500,750,\\fs{font_size+5})\\t(750,900,\\fs{font_size})\\fad(500,0)}}{text}
'''
        # print(dila_str)

    ass_str = f'''[Script Info]
PlayResX: {ratio_w}
PlayResY: {ratio_h}
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: 样式1,{font_name},{font_size},{font_color},&H64000000,&HD6000000,&&HFF000000,0,0,0,0,100,100,0,0,1,2,0,5,15,15,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
{dila_str}

    '''
    return ass_str


def hex_to_ass_color(hex_color):
    # 去除十六进制颜色字符串中的'#'，并转换为十进制数
    hex_color = hex_color[1:]
    ass_color = f'&H00{hex_color[4:6]}{hex_color[2:4]}{hex_color[0:2]}'

    return ass_color




if __name__ == '__main__':
    # 示例用法
    hex_color = "#aaff7f"

    converted_ass_color = hex_to_ass_color(hex_color)

    print(f"ASS to Hex: {hex_color} -> {converted_ass_color}")
