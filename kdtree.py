import numpy as np
import copy
import time
trainset_int = [[2,3],[5,4],[9,6],[4,7],[8,1],[7,2]]
class  TreeNode:
    def  _init(self,x,y):
        self.val1 = x
        self.val2 = y
        self.left = None
        self.right = None
head = None
#对TreeNode进行初始化以及标记head=None
def  sortx(begin,end):
    global  trainset_int
    if end < begin:
        return
#按照横坐标对节点进行分类,使用快排算法对相应节点按照横坐标进行排序
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
    #print('begin = %d,end = %d'%(begin,end))
    if flag == True:
    #按照横坐标对相应的节点进行分类
        sortx(begin,end)
        mid = (begin+end+1)//2
        head = TreeNode()
        head._init(trainset_int[mid][0],trainset_int[mid][1])
        head.left = createtree(head.left,False,begin,mid-1)
        head.right = createtree(head.right,False,mid+1,end)
        return  head
    else:
        sorty(begin,end)
        mid = (begin+end+1)//2
        head = TreeNode()
        head._init(trainset_int[mid][0],trainset_int[mid][1])
        head.left = createtree(head.left,True,begin,mid-1)
        head.right = createtree(head.right,True,mid+1,end)
        return  head
def  preorder(head):
    if  head != None:        
        print('***%d,%d'%(head.val1,head.val2))
        preorder(head.left)
        preorder(head.right)
def  inorder(head):
    if head != None:
        inorder(head.left)
        print('***%d,%d'%(head.val1,head.val2))
        inorder(head.right)
if __name__ == '__main__':
    head = createtree(head,True,0,len(trainset_int)-1)
    print('preorder')
    preorder(head)
    print('inorder')
    inorder(head)
    print('finish')
