#爬取瓜果网页下面对应的所有静态数据
import   requests
from  bs4  import  BeautifulSoup    #用于解析和提取数据
fh = open('data.txt','w',encoding='utf-8')
def  send_request(name,url):
#获取某一个具体的问题以及相应的解答
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    resp = requests.get(url,headers=headers)
    #print(resp.text)
    bs = BeautifulSoup(resp.text,'html.parser')     #得到BeautifulSoup的对象
    #current = bs.find('div',class_='content')
    #question = current.find('p').text
    question = bs.find('h1',class_='title').text
    print(name,end = '***')
    fh.write(name+'***')
    print(question,end = '***')
    #fh = open('data.txt','w',encoding='utf-8')
    fh.write(question+'***')
    #提取出相应的问题
    answer = bs.find_all('div',class_='answer-content')
    #result = []
    flag = False
    for  item  in  answer:
        #print(item)
        current = item.text
        index = current.find('赞')
        current1 = current[0:index]
        current1 = current1.replace('\n','')
        current1 = current1.replace(' ','')
        if  len(current1) == 0:
            continue
        char = current1[0]
        while   len(current1) != 0 and current1[0] == char:
            current1 = current1[1:]
        if  len(current1) == 0:
            continue
        char = current1[len(current1)-1]
        #去除前导的未知字符
        while   1:
            if  len(current1) == 0:
                break
            ends = len(current1)-1
            if  current1[ends] == char:
                current1 = current1[0:ends-1]
            else:
                break
        #去除末尾的未知字符
        #flag用于判断是不是第一个答案，如果为后面的答案需要带上空格
        if  len(current1) == 0:
            continue
        if  flag == False:
            flag = True
            print(current1)
            fh.write(current1)
        else:
            print('    '+current1,end = '') 
            fh.write('    '+current1)
            #result.append(current1+'\n')
    #提取相应的问题以及对应的回答的内容
    print('***',end = '')
    fh.write('***')
    for  item  in  answer:
        item1 = item.find_all('a')
        #找出标签内对应的药品名称
        for  j  in  item1:
            if  j.text.find('赞') == -1 and j.text != '投诉' and j.text != '追答' and j.text != '查看原图' and j.text != '收起':
                print(j.text,end = '    ')
                fh.write(j.text+'    ')
    fh.write('\n')
    print('')
def  getanswerurl(url1):
#查找某一种瓜的所有问题列表
    print(url1)
    url1 = url1[1:]
    pos1 = url1.find('/')
    url1 = url1[pos1+1:]
    pos2 = url1.find('.')
    url1 = url1[:pos2]
    print(url1)
    for  i  in  range(1,100001):
        url = 'https://www.shucai99.com/question/'+url1+'/p/{0}.html'.format(i)
        #佛手瓜对应的问题的网站
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
        resp = requests.get(url,headers=headers)
        bs = BeautifulSoup(resp.text,'html.parser')
        namestring = bs.find('div',class_='breadcrumb').text
        print('###')
        print('###1')
        print(namestring)
        namestring = namestring.replace('\n','')
        pos1 = namestring.find('>')
        namestring = namestring[pos1+1:]
        print('###2')
        print(namestring)
        pos1 = namestring.find('>')
        namestring = namestring[pos1+1:]
        ends = namestring[len(namestring)-1]
        while   1:
            if  namestring[len(namestring)-1] == ends:
                namestring = namestring[:len(namestring)-1]
            else:
                break
        print('namestring = %s###'%namestring)
        #获取到相应的植物的名字
        current = bs.find_all('ul',class_='question-list-col-1')
        #find_all得到的结果为列表，列表中是不能使用find,find_all的
        current_data = current[0]
        #print(current_data)
        current_url_data = current_data.find_all('a')
        if  len(current_url_data) == 0:
            break
        #如果当前页没有a标签了，说明当前页以及后续页都没有内容了
        for   item  in  current_url_data:
            print('https://www.shucai99.com'+item['href'])
            send_request(namestring,'https://www.shucai99.com'+item['href'])
    
def   getallplant():
#获取某一种类别下面的所有的瓜
    url = 'https://www.shucai99.com/question/congsuan.html'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    resp = requests.get(url,headers=headers)
    bs = BeautifulSoup(resp.text,'html.parser')
    current = bs.find_all('ul',class_='category-children')
    #print(current)
    current_data = current[0]
    print(current_data)
    current_url_data = current_data.find_all('a')
    for  item  in  current_url_data:
        print(item['href'])
        getanswerurl(item['href'])
if __name__ == "__main__":
    #send_request('https://www.shucai99.com/question/foshougua/p/1.html')
    #getanswerurl()      #获取某一种植物下面的所有回答
    getallplant()
    fh.close()
