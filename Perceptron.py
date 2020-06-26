# -*- coding: utf-8 -*-
import copy

trainint_set = [[(3,3),1],[(4,3),1],[(1,1),-1]]       #输入数据
w = [0,0]          #初始化w参数
b = 0              #初始化b参数

def update(item):
    global w,b
    w[0] += 1*item[1]*item[0][0]               #w的第一个分量更新
    w[1] += 1*item[1]*item[0][1]               #w的第二个分量更新
    b += 1*item[1]
    print('w = [%d,%d],b = %d'%(w[0],w[1],b))                     #打印出结果

def judge(item):                               #返回y = yi(w*x+b)的结果
    res = 0
    for i in range(len(item[0])):
        res +=item[0][i]*w[i]                   #对应公式w*x
    res += b                                    #对应公式w*x+b
    res *= item[1]                              #对应公式yi(w*x+b)
    return res

def check():                                    #检查所有数据点是否分对了
    flag = False
    for item in trainint_set:
        if judge(item)<=0:                       #如果还有误分类点，那么就小于等于0
            flag = True
            update(item)                         #只要有一个点分错，我就更新
    return flag                                  #flag为False，说明没有分错的了

if __name__ == '__main__':
    flag = False
    for i in range(1000):
        if not check():                            #如果已经没有分错的话
            flag = True
            break
    if flag:
        print('在1000次以内全部分对了')
    else:
        print('很不幸，1000次迭代还是没有分对')
