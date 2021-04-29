"""
图片切割
    # 分割图片
    # 方法1：k-means 4
    # 方法2: 投影(最简单) 当前
    # 方法3：连通域算法
    # 方法3：洪水算法
    # 方法4：滴水算法
"""
import re
from PIL import Image


def save_too_many_value(f_index):
    open("split_too_many_value.txt","a",encoding="utf-8").write(str(f_index)+"\n")
    pass


def split_img(f_index):
    img = Image.open(f"./images_no_lines/color_cleaned_{f_index}.png")
    # 提取色
    width, height = img.size
    set_colors = []
    color_postions = []
    for j in range(width):
        for i in range(height):
            point = img.getpixel((j, i))
            if point not in set_colors:
                set_colors.append(point)
                color_postions.append([])
            color_postions[set_colors.index(point)].append((j, i))

    len_color_postions = [len(color_postion) for color_postion in color_postions]
    max_len_color_postions = max(len_color_postions)
    block_color = set_colors[len_color_postions.index(max_len_color_postions)]
    block_color_postions = color_postions[len_color_postions.index(max_len_color_postions)]
    # 非背景色
    font_postions = [_ for index, color_postion in enumerate(color_postions) for _ in color_postion if
                     index != len_color_postions.index(max_len_color_postions)]

    img_1 = Image.new('RGB', (width, height))
    for j in range(width):
        for i in range(height):
            if (j, i) in block_color_postions:
                img_1.putpixel((j, i), (255, 255, 255))
            else:
                img_1.putpixel((j, i), (0, 0, 0))
    img_1.save(f"./images_bin/split_img_{f_index}_1.png")

    # 图片灰度化
    img_1 = img_1.convert("L")
    # for j in range(width):
    #     for i in range(height):
    #         point = img_1.getpixel((j, i))
    #         print(point, end="")
    #     print()
    threshold = 200
    table = [0 if i < threshold else 1 for i in range(256)]
    img_bin = img_1.point(table, '1')
    # todo 调整方向  先每行在每列
    # for i in range(height):
    #     for j in range(width):
    #         point = L.getpixel((j, i))
    #         print(point, end="")
    #     print()
    # img_1.save("split_img_2.png")

    widths_count = [len([font_postion for font_postion in font_postions if font_postion[0] == _]) for _ in range(width)]
    print(widths_count)
    str_widths_count = "_".join([str(_) for _ in widths_count])
    print(str_widths_count)

    #
    other_str_widths = re.split("(_0)+", str_widths_count)
    # 处理掉嘈杂数据
    other_str_widths = [other_str_width for other_str_width in other_str_widths if
                        other_str_width != "0" and other_str_width != '_0' and other_str_width != '']
    # print(other_str_widths)
    for index, other_str_width in enumerate(other_str_widths):
        # print(str_widths_count.split(other_str_widths[0]))
        try:
            start_str, end_str = str_widths_count.split(other_str_width)
        except ValueError:
            save_too_many_value(f_index)
            break
        start_index, end_index = len(start_str.split("_")), width - len(end_str.split("_")) + 1
        # print(start_index, end_index)
        img_crop = img_bin.crop((start_index, 0, end_index, height))
        img_crop.save(f"./images_split/split_img_{f_index}_2_crop_{index}.png")




if __name__ == '__main__':
    for i in range(8):
        split_img(i)