## 步骤1
  首先读取相应的文本，将其中的标点符号去除掉，然后定义一个vocab统计词语出现次数的字典，接着将字典中顺序出现的词组进行编号，出现次数越多的词组编号越靠前，接着对于所有的此组织计算词频，这里查看了一下论文中的公式，词频要化为原来词频的3/4次方计算的时候效果较好。
## 步骤2
  然后定义了一个Dataset的类，这里面的__getitem__函数每次从中取出单词前面的C个单词以及单词后面的C个单词作为相应的正采样样例，随机抽取单词作为负采样样例，这里面使用了一个nultinomial函数，这是一个pytorch当中的抽取函数，保证了在数组之中词频越高的单词被抽到的几率越大。
## 步骤3
  接下来就是定义EmbeddingModel的对应层了，这里面有两个矩阵，一个是self.in_embed矩阵，负责记录正采样的权重，一个是self.out_embed矩阵，负责提取记录负采样的权重，假设提取正采样的个数为C，负采样的个数为K，B代表每一次的批次数量，则input_embedding = B * embed_size(维度)，pos_embedding = B * (2C) * embed_size(从self.in_embed中取出的正采样的权重值)，neg_embedding = B * (2C * K) * embed_size(从self.out_embed中取出的负采样的权重值)，
Input_embedding = [B,embed_size],pos_embedding = [B,2 * C,embed_size],neg_embedding = [B,2 * K,pos_embedding]，log_pos为input_embedding与pos_embedding相乘，[2 * C,embed_size] * [embed_size,1] = [2 * C,1],所以log_pos = [B,2 * C,1]，化简之后为[B,2 * C]，同理可算出来log_neg，然后使用公式loss = logsigmoid(log_pos)+logsigmoid(log_neg)进行求和，算出对应的损失函数。
## 步骤4
  最后将skip-gram的正采样权重矩阵以及负采样权重矩阵进行训练，训练完成之后取出正采样权重矩阵作为对应的词向量。
关键代码
```python
# 定义PyTorch模型
class EmbeddingModel(nn.Module):
    def __init__(self, vocab_size, embed_size):
    #放入的vocab_size=30000,embed_size=100
        super(EmbeddingModel, self).__init__()
        print('EmbeddingModel __init__')
        self.vocab_size = vocab_size  #30000
        self.embed_size = embed_size  #100
              
        # 模型输入，输出是两个一样的矩阵参数nn.Embedding(30000, 100)
        self.in_embed = nn.Embedding(self.vocab_size, self.embed_size, sparse=False)
        self.out_embed = nn.Embedding(self.vocab_size, self.embed_size, sparse=False)
         # 权重初始化的一种方法
        initrange = 0.5 / self.embed_size
        self.in_embed.weight.data.uniform_(-initrange, initrange)
        self.out_embed.weight.data.uniform_(-initrange, initrange)
        
    def forward(self, input_labels, pos_labels, neg_labels):
        '''
        input_labels: 中心词, [batch_size]
        pos_labels: 中心词周围出现过的单词 [batch_size * (c * 2)],左边找出c个词组，右边找出c个词组
        neg_labelss: 中心词周围没有出现过的单词，从 negative sampling 得到 [batch_size, (c * 2 * K)]
        return: loss, [batch_size]
        '''
        #print('EmbeddingModel forward')
        batch_size = input_labels.size(0) 
       
        input_embedding = self.in_embed(input_labels) # B * embed_size
        pos_embedding = self.out_embed(pos_labels) # B * (2C) * embed_size 
        neg_embedding = self.out_embed(neg_labels) # B * (2*C*K) * embed_size

        log_pos = torch.bmm(pos_embedding, input_embedding.unsqueeze(2)) # B * (2*C)
        log_pos = log_pos.squeeze()
        log_neg = torch.bmm(neg_embedding, -input_embedding.unsqueeze(2)).squeeze() # B * (2*C*K)

        log_pos = F.logsigmoid(log_pos).sum(1)
        log_neg = F.logsigmoid(log_neg).sum(1)
        loss = log_pos + log_neg  # 正样本损失和负样本损失和尽量最大
        #如果为负数的时候就是损失和尽量最小
        #对应的大小为[batch_size]
        #因为需要提取出来的这128个维度的单词集体操作
        return -loss 
        #注意这里return的是-loss，最终的optimizer.step中还带有一个减号
        #所以这里如果是当前选中的这个单词的周边单词的话的128个维度单词的梯度被减去，而周边单词的梯度被加上，
        #而如果是这128个单词负采样的话这128个维度的单词
    
    # 模型训练有两个矩阵，self.in_embed和self.out_embed两个, 作者认为输入矩阵比较好，舍弃了输出矩阵
    # 取出输入矩阵参数，self.in_embed的矩阵为正采样的相应的矩阵，self.out_embed为负采样的相应矩阵
    def input_embeddings(self):   
        return self.in_embed.weight.data.cpu().numpy() 
    def output_embeddings(self):
        return self.out_embed.weight.data.cpu().numpy()
```
