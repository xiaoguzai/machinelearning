import numpy as np
import copy
import time
trainint_set = [[(3,3),1],[(4,3),1],[(1,1),-1]]       #输入数据
a = [] 
b = 0
gram = [[0 for _ in range(len(trainint_set))]for _ in range(len(trainint_set))]
def  getgram():
    global  gram
    cur1 = [[0 for _ in range(2)]for _ in range(len(trainint_set))]
    cur2 = [[0 for _ in range(len(trainint_set))]for _ in range(2)]
    for  i  in  range(len(trainint_set)):
        cur1[i][0] = trainint_set[i][0][0]
        cur1[i][1] = trainint_set[i][0][1]
    '''
    形成[3,3
        4,3
        1,1]的矩阵
    '''
    for  i  in  range(len(trainint_set)):
        cur2[0][i] = trainint_set[i][0][0]
        cur2[1][i] = trainint_set[i][0][1]
    '''
    形成[3,4,1
        3,3,1]的矩阵
    '''
    for  i  in  range(len(trainint_set)):
        for  j  in  range(len(trainint_set)):
            gram[i][j] += np.dot(cur1[i][0],cur2[0][j])
            gram[i][j] += np.dot(cur1[i][1],cur2[1][j])
    '''形成相应的gram矩阵'''
def  judge(k,item):
#判断当前的点的坐标是否被误分类
    global  a,b,trainint_set
    #使用item进行判断
    current = 0
    for  i  in  range(len(trainint_set)):
    #遍历trainint_set数组,找寻相应的数值
        current = current+a[i]*trainint_set[i][1]*gram[k][i]
    #使用误分条件yi*(ai*yi*gram[k][i]+b)
    current = current+b
    current = current*item[k][1]
    #print('!!!k = %d,current = %d'%(k,current))
    if  current > 0:
        return  True
    else:
    #<=0时为误分类点
        return  False
def  update(k,item):
#在误分类的情况下更新当前节点的坐标
    global  a,b
    a[k] = a[k]+1
    b = b+item[k][1]
if __name__ == '__main__':
    for  i  in  range(len(trainint_set)):
        a.append(0)
    #初始化a对应的数组，其中a数组的长度与trainint_set的长度一致
    getgram()
    cur = 0
    while   cur < len(trainint_set):
        if  judge(cur,trainint_set) == False:
            update(cur,trainint_set)
        #更新对应的a,b数值
            cur = 0
        else:
            cur = cur+1
    w = []
    w1,w2 = 0,0
    print('***%d,%d,%d'%(a[0],a[1],a[2]))
    for  i  in  range(len(trainint_set)):
        w1 +=a[i]*trainint_set[i][0][0]*trainint_set[i][1]
    for  i  in  range(len(trainint_set)):
        w2 +=a[i]*trainint_set[i][0][1]*trainint_set[i][1]
    w.append(w1)
    w.append(w2)
    print('results = ***')
    print('w = %d,%d'%(w[0],w[1]))
    print('b = %d'%b)

