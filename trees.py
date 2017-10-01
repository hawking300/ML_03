from math import log
import operator

def calcShannonEnt(dataSet):
    """求样本空间的香农熵"""
    numEntries = len(dataSet)#确定样本总数
    labelCounts = {}#建立一个分类的字典
    for featVec in dataSet:#遍历样本库，求出每个分类的样本数
        currentLabel = featVec[-1]#取出数据库的最后一个标签作为分类向量
        if currentLabel not in labelCounts.keys():
            #如果分类字典没有这个向量，就建立这个向量并赋值0。
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
        #如果字典有这个分类，就计数，得出某个分类的样本总数
    shonnonEnt = 0.0
    for key in labelCounts:#遍历字典，求出每个分类的香农熵，最后求总和
        prob = float(labelCounts[key])/numEntries#求每个分类的概率分布
        shonnonEnt -= prob * log(prob, 2)#求香农熵
    return shonnonEnt
def classify(input_tree, feat_labels, test_vec):
    # first_str = input_tree.keys()[0]
    first_sides = list(input_tree.key())
    first_str = first_sides
    second_dict = input_tree[first_str]
    feat_index = feat_labels.index(first_str)
    for key in second_dict.keys():
        if test_vec[feat_index] == key:
            if type(second_dict[key]).__name__ =='dict':
                class_label = classify(second_dict[key],feat_labels,test_vec)
            else:
                class_label = second_dict[key]
    return class_label
def createDataSet():
    dataSet = [[1,1,'yes'],
               [1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no']]
    labels = ['no surfaceing','flippers']
    return dataSet,labels
def createTree(dataSet ,labels,my_gamePoint):
    """建立决策树算法。
        dataSet是训练样本集，labels是分类标签向量"，my_gamePoint 是递归次数计数器
    """
    my_gamePoint[0] +=1
    #取出递归当前dataSet的最后一位标签的值放到classlist
    classList = [example[-1] for example in dataSet]
    """第一个停止条件：计算标签的长度，如果标签长度等于第一个标签的值的数量，说明标签都是一样的
       说明该节点包含的值都是一种类型，停止递归，作为叶节点
    """
    if classList.count(classList[0]) == len(classList):

        return classList[0]
    """第二个停止条件：特征使用完了，但是数据集还有剩下的数据。利用majorityCnt投票
        选出属性值最多的标签，作为子节点。继续递归直到找到叶节点。
    """
    if len(dataSet[0])== 1:

        return majorityCnt(classList)
    #如果不符合停止条件，则继续，计算最佳信息增益的特征
    bestFeat = chooseBestFeatureToSplit(dataSet)
    #获得最佳信息增益的特征的标签的值
    bestFeatLabel = labels[bestFeat]
    #在决策树里记录最佳信息增益的标签，作为递归过程的根节点或子节点
    myTree = {bestFeatLabel:{}}
    #把这个根节点的标签删除，以便继续递归计算子节点。
    del(labels[bestFeat])
    #提取子节点中最佳信息增益的特征的取值
    featValues = [example[bestFeat] for example in dataSet]
    #把上述特征的取值通过set进行去除重复的值，留下不重复的值。
    uniqueVals = set(featValues)
    #遍历上述取值，递归计算下一个子节点
    for value in uniqueVals:
        #列出子节点里还有多少标签
        subLabels = labels[:]
        #以最佳信息增益的特征为基准特征，分割数据集，获得新数据集（包括相应的属性值）
        #以新的数据集和剩余标签为参数，递归建立新的子节点，直到满足上述停止条件
        myTree[bestFeatLabel][value] = createTree(splitDataSet\
                                        (dataSet,bestFeat,value),
                                                  subLabels,my_gamePoint)
    return myTree, my_gamePoint
def chooseBestFeatureToSplit(dataSet):
    """找到最好的划分数据集的方式"""
    numFeatures = len(dataSet[0])-1#计算特征数量，最后一个是标签，所以去掉
    baseEntropy = calcShannonEnt(dataSet)#求样本空间的经验熵
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):#按不同的特征遍历dataSet
        featList = [example[i] for example in dataSet]
        #for循环，遍历dataSet，返回列表的每元素的第i个项，并以此赋值给新的列表featList
        #本行是找出第i个特征的所有取值
        uniqueVals = set(featList)
        #set返回一个去掉重复值的集合，每次循环增加不重复的值
        #本节是针对不同的特征建立一个不重复的取值范围
        newEntropy = 0.0
        for value in uniqueVals:#计算每个特征的不同取值的条件概率和条件熵的和
            subDataSet = splitDataSet(dataSet, i, value)
            #按特征值的不同取值划分数据集
            prop = len(subDataSet)/float(len(dataSet))
            #计算该特征的每个取值的条件概率
            newEntropy += prop * calcShannonEnt(subDataSet)
            #计算每个特征的熵及其和，即条件熵
        infoGain = baseEntropy-newEntropy#计算信息增益
        if (infoGain> bestInfoGain):#找出最大的信息增益
            bestInfoGain = infoGain
            bestFeature = i#标记最大信息增益的特征值
    return bestFeature
def majorityCnt(classList):
    """"""
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key = operator.itemgetter(
        1),reverse = True)
    return sortedClassCount[0][0]


def splitDataSet(dataSet,axis,value):
    """
    分割数据集，三个参数是待分割数据集，特征，需要返回的特征值
    按特征axis的取值value来分割数据集，得到一个特征取值为value的子集，
    该子集的元素是不包含value的其他内容，包括其他特征的取值等

    """
    retDataSet = []#建立一个新的数据列表，不直接调用原有数据列表，防止更改原数据列表
    for featVec in dataSet:#从列表中取出一个元素，最终遍历整个列表
        if featVec[axis] == value:
            #寻找列表中每个元素的第axis项中符合特征值的元素
            #下面把符合特征值的切片后，放到新的列表中，切片是去掉特征AXIS，保留前后面其他部分
            reduceFeatVec = featVec[:axis]
            #返回一个从0到axis-1的列表切片，axis=0，返回空表。
            #如果不等于0，返回axis前面的部分，等于是把axis前面切片
            reduceFeatVec.extend(featVec[axis+1:])
            #把该元素的axis项后边的内容用extend方法添加到新列表的后边，
            # extend是把源列表的每项内容都单独作为新表的一项内容
            #featvec[axis+1:]作用是把axis后面切片。
            retDataSet.append(reduceFeatVec)
            #append方法是把新列表整体作为一项添加到另一个列表中
    return retDataSet






#main
myDataSet, myLabels = createDataSet()
myTree, my_gamePoint= createTree(myDataSet,myLabels,[0])
# print(myTree)
# print((my_gamePoint))


# dataSet, labels = createDataSet()
# i = chooseBestFeatureToSplit(dataSet)
# print(i)
# calcShannonEnts = calcShannonEnt(dataSet)
# splitDataSet(dataSet,0,1)
# print(calcShannonEnts)
