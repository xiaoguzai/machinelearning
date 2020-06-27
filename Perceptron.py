import copy
import time
trainint_set = [[(3,3),1],[(4,3),1],[(1,1),-1]]       #输入数据
w = [0,0]          #初始化w参数
b = 0              #初始化b参数
#测试集中的数据始终不发生变化
def  change(item):
    global  w,b
    w[0] = w[0]+item[1]*item[0][0]
    w[1] = w[1]+item[1]*item[0][1]
    b = b+item[1]
#使用梯度下降算法更新每次前面的系数,每次更新的时候w = w+y*x,b = b+y
def  judge(item):
    result = item[1]*(item[0][0]*w[0]+item[0][1]*w[1]+b)
    if  result > 0:
        return  True
    else:
        return  False
if __name__ == '__main__':
    cur = 0
    while cur < len(trainint_set):
        item = trainint_set[cur]
        if  judge(item) == False:
            change(item)
            cur = 0
        else:
            cur = cur+1
    print('results = %d,%d,%d'%(w[0],w[1],b))
