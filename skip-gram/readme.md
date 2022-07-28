## 步骤1
  首先读取相应的文本，将其中的标点符号去除掉，然后定义一个vocab统计词语出现次数的字典，接着将字典中顺序出现的词组进行编号，出现次数越多的词组编号越靠前，接着对于所有的此组织计算词频，这里查看了一下论文中的公式，词频要化为原来词频的3/4次方计算的时候效果较好。
## 步骤2
  然后定义了一个Dataset的类，这里面的__getitem__函数每次从中取出单词前面的C个单词以及单词后面的C个单词作为相应的正采样样例，随机抽取单词作为负采样样例，这里面使用了一个nultinomial函数，这是一个pytorch当中的抽取函数，保证了在数组之中词频越高的单词被抽到的几率越大。
## 步骤3
  接下来就是定义EmbeddingModel的对应层了，这里面有两个矩阵，一个是self.in_embed矩阵，负责记录正采样的权重，一个是self.out_embed矩阵，负责提取记录负采样的权重，假设提取正采样的个数为C，负采样的个数为K，B代表每一次的批次数量，则input_embedding = B * embed_size(维度)，pos_embedding = B * (2C) * embed_size(从self.in_embed中取出的正采样的权重值)，neg_embedding = B * (2C * K) * embed_size(从self.out_embed中取出的负采样的权重值)，
Input_embedding = [B,embed_size],pos_embedding = [B,2 * C,embed_size],neg_embedding = [B,2 * K,pos_embedding]，log_pos为input_embedding与pos_embedding相乘，[2 * C,embed_size] * [embed_size,1] = [2 * C,1],所以log_pos = [B,2 * C,1]，化简之后为[B,2 * C]，同理可算出来log_neg，然后使用公式loss = logsigmoid(log_pos)+logsigmoid(log_neg)进行求和，算出对应的损失函数。
## 步骤4
	最后将skip-gram的正采样权重矩阵以及负采样权重矩阵进行训练，训练完成之后取出正采样权重矩阵作为对应的词向量。

