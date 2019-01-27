import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

class genetic_algorithm(object):
    
    def __init__(self,population_num,dim,n_cross):
        #染色体数
        self.population_num = population_num
        #染色体维数
        self.dim = dim
        #染色体交叉时基因片段的长度
        self.n_cross = n_cross
        #最大迭代次数
        self.iter = 33
        #初始化染色体组
        self.population = np.random.rand(population_num,dim)
    
    #========= 需要优化的函数（计算适应度） =======      
    def f(self,x):
        weighted_item = np.dot(add,x)

        X = pd.concat([base,pd.DataFrame(weighted_item)],axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
        X_train_scale = preprocessing.scale(X_train)
        X_test_scale = preprocessing.scale(X_test)

        clf = RandomForestClassifier(n_estimators=5, max_depth=4,random_state=42)
        clf.fit(X_train_scale,y_train)

        return clf.score(X_test_scale,y_test)
        #return np.sin(4*x[0])
    #================================
    
    def weight_scaler(self,weight):   #将权重组（染色体）归一化
        scale_weight_list = [weight[i]/weight.sum(axis=1)[i] for i in range(self.population_num)]
        scale_weight_arr = np.vstack(scale_weight_list)
        return scale_weight_arr
    
    def cal_f_value_scale(self,weight):   #计算每个染色体的适应值
        scale_weight_arr = self.weight_scaler(weight)
        func_value_list = [self.f(scale_weight_arr[i]) for i in range(self.population_num)]
        func_value_scale = [func_value_list[i]/sum(func_value_list) for i in range(self.population_num)]
        return func_value_scale
    
    def find_weight_index(self,rand_f_value,func_value_scale):   #找到轮盘取样对应的染色体在染色体组的位置
        length=0
        i=0
        while length<rand_f_value:
            length = length + func_value_scale[i]
            i = i+1
        return i-1
    
    def get_parent_weight(self,weight):   #得到父辈染色体
        #生成0到1的随机数组，个数与染色体组大小相同
        temp = np.random.rand(self.population_num)
        #此处直接计算function value，避免在运行find_weight_index时重复调用
        func_value_scale = self.cal_f_value_scale(weight)
        #适应度高的染色体容易被抽到，通过调用find_weight_index函数，找到其权重向量
        index_list = [self.find_weight_index(temp[i],func_value_scale) for i in range(self.population_num)]
        #在原始权重中找到对应下标的权重
        scale_weight = self.weight_scaler(weight)
        target_weight = scale_weight[index_list]
        #打乱新生成的100个权重，分成两半，一组为父染色体，一组为母染色体
        arr = np.arange(self.population_num)
        np.random.shuffle(arr)
        shuffled_weight = target_weight[arr]
        father = shuffled_weight[:self.population_num//2]
        mother = shuffled_weight[self.population_num//2:]
        return father,mother
    
    def cross_over(self,weight):   #交叉父辈染色体片段，得到子代染色体
        father,mother = self.get_parent_weight(weight)
        for i in range(self.population_num//2):
            #生成基因个数长度的随机整数组，交换亲代染色体对应下标的基因片段
            rand = np.random.randint(0,self.dim,self.population_num)
            par1 = father[i]
            par2 = mother[i]
            par1[rand],par2[rand] = par2[rand],par1[rand]
        sons = np.vstack([father,mother])
        return sons
    
    def iteration(self):  #不断迭代
        #将初始染色体交叉
        sons = self.cross_over(self.population)
        N=0
        max_iter = self.iter
        content = []  #记录迭代过程中的染色体
        mean_f_list = []
        while N<max_iter:
            scale_weight_arr = self.weight_scaler(sons)
            func_value_list = [self.f(scale_weight_arr[i]) for i in range(self.population_num)]
            mean_f = sum(func_value_list)/len(func_value_list)#/n_sample
            mean_f_list.append(mean_f)
            print(mean_f)
            sons = self.cross_over(sons)
            #var = sum([sons[:,i].std() for i in range(self.n_weight)])/self.n_weight
            N = N + 1
            if N%2==0:
                content.append(sons)
            else:
                pass
        return sons,content,mean_f_list
    
    def func_value_plot(self):
        sons,content,mean_f_list = self.iteration()
        plt.plot(mean_f_list)
        plt.xlabel('iteration')
        plt.ylabel('scores')
        
if __name__ == '__main__':
    #数据处理
    data = pd.read_excel('回归数据2.xlsx')
    base_list = ['实际资本','参考利率']
    add_list = ['加入协会','ICP认证','上市参股','银行存管1']
    base = data[base_list]
    add = data[add_list]
    y = data['label']
    #迭代计算
    ga = genetic_algorithm(100,len(add_list),2)
    result,content,mean_f_list = ga.iteration()
    plt.plot(mean_f_list)
    plt.show()