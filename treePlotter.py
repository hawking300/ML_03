import matplotlib.pyplot as plt

# 定义文本框和箭头形式
# boxstyle:边框的样式;fc:底色的颜色;alpha:颜色的深浅程度
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc='0.8')
# arrowstyle:线段的样式; connectionstyle:线段的展示形式(曲线、圆弧) color:线段颜色
arrow_args = dict(arrowstyle="<-")


def create_plot(my_tree):
    """绘制决策树"""
    # 指定默认中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['font.family'] = 'sans-serif'
    # 解决负号'-'显示为方块的问题
    plt.rcParams['axes.unicode_minus'] = False
    # 建立一个画布
    fig = plt.figure(1, facecolor='white')
    # 清空画布
    fig.clf()
    ax_props = dict(xticks=[],yticks = [])
    # 在画布里按指定区域开始画图
    create_plot.axl = plt.subplot(111, frameon=False, **ax_props)
    plot_tree.totalW = float(get_num_leafs(my_tree))
    plot_tree.totalD = float(get_tree_depth(my_tree))
    plot_tree.xOff = -0.5/plot_tree.totalW
    plot_tree.yOff = 1.0
    plot_tree(my_tree,(0.5,1.0), '')
    plt.show()


def get_num_leafs(my_tree):
    """计算叶子数.
    Args：
        my_tree:决策树的字典
    """
    num_leafs = 0
    # 获得树字典里的第一个元素的KEY的名字
    first_sides = list(my_tree.keys())
    first_str = first_sides[0]  # 找到输入的第一个元素
    # first_str = my_tree.keys()[0]
    # python3改变了dict.keys, 返回的是dict_keys对象, 支持iterable
    # 但不支持indexable，我们可以将其明确的转化成list，

    # 把第一个元素的KEY的取值VALUE作为一个新的字典
    second_dict = my_tree[first_str]
    # 遍历新的字典
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            num_leafs += get_num_leafs(second_dict[key])
        else:
            num_leafs += 1
    return num_leafs


def get_tree_depth(my_tree):
    max_depth = 0
    # first_str = my_tree.keys()[0]
    first_sides = list(my_tree.keys())
    first_str = first_sides[0]  # 找到输入的第一个元素
    second_dict = my_tree[first_str]
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            this_depth = 1 + get_tree_depth(second_dict[key])
        else:
            this_depth = 1
        if this_depth > max_depth:
            max_depth = this_depth
    return max_depth


def plot_node(node_txt, center_pt, parent_pt, node_type):
    """"绘制节点图

    :param node_txt: 标签的内容
    :param center_pt: 标签的位置
    :param parent_pt: 注释的位置，即一个指向某个节点的注释
    :param node_type: 节点于注释之间连线的样式

    :return:
        xycoords 和textcoords 表示xy点和xytext点的相关注释说明;
        arrowprops连线的样式

    """
    create_plot.axl.annotate(node_txt, xy=parent_pt, xycoords='axes fraction',
                             xytext=center_pt, textcoords='axes fraction',
                             va='center', ha='center', bbox=node_type,
                             arrowprops=arrow_args)
    # annotate方法是对图片进行注释
    # 第一个参数是注释的内容
    # xy： 设置箭头尖的坐标
    # xytext: 设置注释内容显示的起始位置
    # arrowprops 用来设置箭头
    # facecolor 设置箭头的颜色
    # headlength 箭头的头的长度
    # headwidth 箭头的宽度
    # width 箭身的宽度
    # plt.annotate(u"This is a zhushi", xy = (0, 1), xytext = (-4, 50),\
    # arrowprops = dict(facecolor = "r", headlength = 10, headwidth
    # = 30, width = 20))
    # 可以通过设置xy和xytext中坐标的值来设置箭身是否倾斜


def plot_mid_text(cntr_pt, parent_pt, txt_string):
    # 在父子节点间填充信息.
    x_mid = (parent_pt[0] - cntr_pt[0]) / 2.0 + cntr_pt[0]
    y_mid = (parent_pt[1] - cntr_pt[1]) / 2.0 + cntr_pt[1]

    create_plot.axl.text(x_mid, y_mid, txt_string)


def plot_tree(my_tree, parent_pt, node_txt):
    """
    绘制决策树
    :param my_tree: 待绘制的决策树
    :param parent_pt: 父节点
    :param node_txt: 父节点文本
    :return:
    """
    # 计算宽和高
    num_leafs = get_num_leafs(my_tree)
    depth = get_tree_depth(my_tree)
    #寻找父节点，并记录名字
    # first_str = my_tree.keys()[0]
    first_sides = list(my_tree.keys())
    first_str = first_sides[0]  # 找到输入的第一个元素
    #计算节点的坐标值，每个叶子左右各有一个空挡，总空挡是2*叶子数
    cntr_pt = (plot_tree.xOff + (1.0 + float(
        num_leafs)) / 2.0 / plot_tree.totalW, plot_tree.yOff)
    plot_mid_text(cntr_pt, parent_pt, node_txt)#
    plot_node(first_str, cntr_pt, parent_pt, decisionNode)
    second_dict = my_tree[first_str]
    plot_tree.yOff = plot_tree.yOff - 1.0 / plot_tree.totalD
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == 'dict':
            plot_tree(second_dict[key], cntr_pt, str(key))
        else:
            plot_tree.xOff = plot_tree.xOff + 1.0 / plot_tree.totalW
            plot_node(second_dict[key], (plot_tree.xOff, plot_tree.yOff),
                     cntr_pt, leafNode)
            plot_mid_text((plot_tree.xOff, plot_tree.yOff), cntr_pt, str(key))
    plot_tree.yOff = plot_tree.yOff + 1.0 / plot_tree.totalD


def retrieve_tree(i):
    list_of_trees = [{'no surfacing': {0: 'no', 1: {'flippers':
                                                        {0: 'no',
                                                         '1': 'yes'}}}},
                     {'no surfacing': {0: 'no', 1: {'flippers':
                                                        {0: {'head': {0: 'no',
                                                                      1: 'yes'}},
                                                         1: 'no'}}}}

                     ]
    return list_of_trees[i]


"""main"""

my_tree = retrieve_tree(0)
my_tree['no surfacing'][3] = 'maybe'
create_plot(my_tree)

# create_plot()
