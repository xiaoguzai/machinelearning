import numpy as np
import copy
import time
trainset_int = [[6.27,5.50],[1.24,-2.86],[-6.88,-5.40],[-4.60,-10.55],[-2.96,-0.50],[-4.96,12.61],[1.75,12.26],
[17.05,-12.79],[7.75,-22.68],[15.31,-13.16],[10.80,-5.03],[7.83,15.70],[14.63,-0.35]]
result = []
posx,posy = -1.0,-5.0
num = 3
class  TreeNode:
    def  _init(self,x,y):
        self.val1 = x
        self.val2 = y
        self.visit = False
        self.left = None
        self.right = None
head = None
#对TreeNode进行初始化以及标记head=None

def  sortx(begin,end):
#按照横坐标对节点进行分类,使用快排算法对相应节点按照横坐标进行排序
    global  trainset_int
    if end < begin:
        return
    pivot = trainset_int[begin]
    left,right = begin,end
    while   left < right:
        while   left < right and trainset_int[right][0] >= pivot[0]:
            right = right-1
        trainset_int[left] = trainset_int[right]
    #这里left不主动移动的原因是下面对left进行循环移动，从而避免越界的现象发生
        while   left < right and trainset_int[left][0] <= pivot[0]:
            left = left+1
        trainset_int[right] = trainset_int[left]
    #right不主动移动的原因是下面对left进行循环移动，从而避免越界的现象发生
    #print('left = %d,right = %d'%(left,right))
    trainset_int[left] = pivot
    sortx(begin,left-1)
    sortx(left+1,end)

def  sorty(begin,end):
    global  trainset_int
    #按照纵坐标对节点进行分类
    if end < begin:
        return
    pivot = trainset_int[begin]
    left,right = begin,end
    while   left < right:
        while   left < right and trainset_int[right][1] > pivot[1]:
            right = right-1
        trainset_int[left] = trainset_int[right]
        while   left < right and trainset_int[left][1] < pivot[1]:
            left = left+1
        trainset_int[right] = trainset_int[left]
    trainset_int[left] = pivot
    sorty(begin,left-1)
    sorty(left+1,end)

def  createtree(head,flag,begin,end):
    #head代表当前正在找寻的节点,flag标记是按照横坐标分类还是按照纵坐标分类
    #begin和end标记对应数组的开始位置以及结束位置'''
    if end < begin:
        return  None
    if flag == True:
    #按照横坐标对相应的节点进行分类
    #flag == True的情况下下面根据x坐标排序进行分类
    #左孩子为x节点坐标比根节点小的坐标，右孩子为x节点坐标比根节点大的坐标
        sortx(begin,end)
        mid = (begin+end)//2
        #这里也可以写作mid = (begin+end+1)//2,李航老师的书中是带+1这一步的
        head = TreeNode()
        head._init(trainset_int[mid][0],trainset_int[mid][1])
        head.left = createtree(head.left,False,begin,mid-1)
        head.right = createtree(head.right,False,mid+1,end)
        return  head
    else:
    #按照纵坐标对相应的节点进行分类
    #根节点为mid对应的内容，放置中间位置对应的数值
        sorty(begin,end)
        mid = (begin+end)//2
        #这里也可以写作mid = (begin+end+1)//2,李航老师的书中是带+1这一步的
        head = TreeNode()
        head._init(trainset_int[mid][0],trainset_int[mid][1])
        head.left = createtree(head.left,True,begin,mid-1)
        head.right = createtree(head.right,True,mid+1,end)
        return  head
def  preorder(head):
    if  head != None:        
        print('***%f,%f'%(head.val1,head.val2))
        preorder(head.left)
        preorder(head.right)
def  inorder(head):
    if head != None:
        inorder(head.left)
        print('***%f,%f'%(head.val1,head.val2))
        inorder(head.right)
def  sortarray():
#将数组中离点(posx,posy)距离最大的点放置到数组的最后位置
    global  posx,posy
    maxdis = (result[0][0]-posx)*(result[0][0]-posx)+(result[0][1]-posy)*(result[0][1]-posy)
    maxpos = 0
    for  i  in  range(1,len(result)):
        currentdis = (result[i][0]-posx)*(result[i][0]-posx)+(result[i][1]-posy)*(result[i][1]-posy)
        if  currentdis > maxdis:
            maxdis = currentdis
            maxpos = i
    temp = result[len(result)-1]
    result[len(result)-1] = result[maxpos]
    result[maxpos] = temp

def  calculatedis(currentx,currenty):
#计算当前的坐标是否可以被放入结果数组result之中,如果当前的数组未满的时候直接放入
#如果当前的数组已经放满的时候看放入坐标离最近坐标的距离是否比当前数组
    if  len(result) < num:
        result.append([currentx,currenty])
        sortarray()
    else:
        currentdis1 = (result[len(result)-1][0]-posx)*(result[len(result)-1][0]-posx)+(result[len(result)-1][1]-posy)*(result[len(result)-1][1]-posy)
        currentdis2 = (currentx-posx)*(currentx-posx)+(currenty-posy)*(currenty-posy)
        if  currentdis2 < currentdis1:
            result[len(result)-1] = [currentx,currenty]
            sortarray()

def  searchtree(head,flag):
#按照不同的flag对相应节点的数值进行查找
    global  posx,posy,num
    if  len(trainset_int) == 1:
        result.append(trainset_int[0])
        return
    if  head == None:
        return 
    if  head.left == None  and  head.right != None:
    #只有一个节点的时候无需比较，直接访问相应的节点
        searchtree(head.right,bool(1-flag)) 
        head.visit = True
        calculatedis(head.val1,head.val2)
    elif    head.left != None  and  head.right == None:
    #右子树不为空的时候对右子树进行搜索，计算相应的距离
        searchtree(head.left,bool(1-flag))
        head.visit = True
        calculatedis(head.val1,head.val2)
    elif    head.left != None  and  head.right != None:
        #左右子树都不为空的情况下
        if  flag == True:
        #以x为分界点的情况下
            if  posx < head.val1:
                searchtree(head.left,bool(1-flag))
                head.visit = True
                calculatedis(head.val1,head.val2)
                maxdis = (result[len(result)-1][0]-posx)*(result[len(result)-1][0]-posx)+(result[len(result)-1][1]-posy)*(result[len(result)-1][1]-posy)
                if  maxdis > (posx-head.val1)*(posx-head.val1):
                    searchtree(head.right,bool(1-flag))
            #分析右边是否可以找出比当前最大值要小的距离
            else:
                searchtree(head.right,bool(1-flag))
                head.visit = True
                calculatedis(head.val1,head.val2)
                maxdis = (result[len(result)-1][0]-posx)*(result[len(result)-1][0]-posx)+(result[len(result)-1][1]-posy)*(result[len(result)-1][1]-posy)
                if  maxdis > (posx-head.val1)*(posy-head.val1):
                    searchtree(head.left,bool(1-flag))
            #分析左边是否可以找出比当前最大值要小的距离
        else:
            #以y为分界点的情况下
            #这里之前报invalid syntax,仔细看前面发现是上面行出现的searchtree函数后面少了个括号
            if  posy < head.val2:
                searchtree(head.left,bool(1-flag))
                head.visit = True
                calculatedis(head.val1,head.val2)
                maxdis = (result[len(result)-1][0]-posx)*(result[len(result)-1][0]-posx)+(result[len(result)-1][1]-posy)*(result[len(result)-1][1]-posy)
                if  maxdis > (posy-head.val2)*(posy-head.val2):
                    searchtree(head.right,bool(1-flag))
            #分析右子树(上面)是否可以找出比当前最大值要小的距离
            else:
                searchtree(head.right,bool(1-flag))
                head.visit = True
                calculatedis(head.val1,head.val2)
                maxdis = (result[len(result)-1][0]-posx)*(result[len(result)-1][0]-posx)+(result[len(result)-1][1]-posy)*(result[len(result)-1][1]-posy)
                if  maxdis > (posy-head.val2)*(posy-head.val2):
                    searchtree(head.left,bool(1-flag))
            #分析左子树(下面)是否可以找出比当前最大值要小的距离
            #如果有可能的话(对应距离画出来的圆的半径跨越过分界点的时候)需要继续查找另一半
    else:
        #达到一个底部节点时
        head.visit = True
        calculatedis(head.val1,head.val2)
if __name__ == '__main__':
    head = createtree(head,True,0,len(trainset_int)-1)
    print('preorder')
    preorder(head)
    print('inorder')
    inorder(head)
    #print('begin search')
    searchtree(head,True)
    #print('after search')
    for  i  in  range(len(result)):
        print('(%f,%f)'%(result[i][0],result[i][1]),end = ' ')
    print('')
