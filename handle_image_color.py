from PIL import Image


def test(fi):
    img = Image.open(f"./images/test_{fi}.png")
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
    # 仅仅需要展示
    show_set_colors = []
    show_color_postions = []
    for index, set_color in enumerate(set_colors):
        if len(color_postions[index]) < 10:
            continue
        show_set_colors.append(set_color)
        show_color_postions.append(color_postions[index])
        # print(set_color, len(color_postions[index]))

    # # 图像展示
    # for index, show_set_color in enumerate(show_set_colors):
    #     print(show_set_color)
    #     img = Image.new('RGB', (width, height))
    #     for j in range(width):
    #         for i in range(height):
    #             if (j, i) in show_color_postions[index]:
    #                 img.putpixel((j, i), show_set_color)
    #             else:
    #                 img.putpixel((j, i), (255, 255, 255))
    #     img.save(f"color_{index}.png")

    # 去除掉线段(线段的域比较大，上下线)

    def get_min_max(show_color_postions):
        r_area = []
        for show_color_postion in show_color_postions:
            # 每一个都有很多个坐标
            widths = []
            heights = []
            [[widths.append(color_postion[0]), heights.append(color_postion[1])] for color_postion in
             show_color_postion]
            max_min_width = max(widths), min(widths)
            max_min_height = max(heights), min(heights)
            area = (max_min_width[0] - max_min_width[1]) * (max_min_height[0] - max_min_height[1])
            r_area.append(area)
        return r_area

    def get_width_limit(show_color_postions, width):
        bool_width = []
        for show_color_postion in show_color_postions:
            # 每一个都有很多个坐标
            widths = []
            [[widths.append(color_postion[0])] for color_postion in show_color_postion]
            max_min_width = max(widths), min(widths)
            bool_width.append(max_min_width[0] - max_min_width[1])
        print(width)
        bool_width = [False if (int(_width) > int(width / 2)) else True for _width in bool_width]
        return bool_width

    # print(max_min_show_color_postions)
    end_shows_areas = get_min_max(show_color_postions)
    del_shows_areas = sorted(end_shows_areas, reverse=True)[:-4]
    # 根据面积
    bool_end_shows = [False if end_shows_area in del_shows_areas else True for end_shows_area in end_shows_areas]
    print("面积", bool_end_shows)
    # 根据面积获取背景色
    print("背景id", bool_end_shows.index(max(bool_end_shows)) - 1)
    block_color = show_set_colors[0]
    print("背景色 --->", block_color)
    # 根据宽度
    bool_end_shows_width = get_width_limit(show_color_postions, width)

    bool_end_shows = [False if bool_end_shows_width[index] != bool_end_show else bool_end_show for index, bool_end_show
                      in
                      enumerate(bool_end_shows)]

    print(end_shows_areas)
    print("宽度", bool_end_shows_width)
    print("求和", bool_end_shows)

    # print(del_shows_areas)
    # print("_")
    # print(end_shows_areas)

    new_show_set_colors = [show_set_color for index, show_set_color in enumerate(show_set_colors) if
                           bool_end_shows[index]]
    new_show_color_postions = [show_color_postion for index, show_color_postion in enumerate(show_color_postions) if
                               bool_end_shows[index]]

    # 调整颜色为背景色
    clean_color_postions = [_ for index, show_color_postion in enumerate(show_color_postions) for _ in
                            show_color_postion if
                            not bool_end_shows[index]]

    # for index, show_set_color in enumerate(new_show_set_colors):
    #     print(show_set_color)
    #     img = Image.new('RGB', (width, height))
    #     for j in range(width):
    #         for i in range(height):
    #             if (j, i) in new_show_color_postions[index]:
    #                 img.putpixel((j, i), show_set_color)
    #             else:
    #                 img.putpixel((j, i), (255, 255, 255))
    #     img.save(f"color_del_two_{index}.png")
    print("绘图-->")
    for j in range(width):
        for i in range(height):
            if (j, i) in clean_color_postions:
                img.putpixel((j, i), block_color)
    img.save(f"./images_no_lines/color_cleaned_{fi}.png")


if __name__ == '__main__':
    for fi in range(0, 8, 1):
        test(fi)
        # break
