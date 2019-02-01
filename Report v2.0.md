

[TOC]

# Report 2019.2.1

## Intro

​	本轮测试尝试将数据集分为两部分：三个“基础变量”与一个“附加变量”。“基础变量”指代网贷平台的共有属性，以连续变量为主，“附加变量”指代网贷平台的特殊属性，由若干个离散变量加权而成。

​	具体而言，本文从剔除三个“基础变量”后的剩余变量中选取表现较好的若干个变量加权形成"附加变量"。之后将"基础变量"与"附加变量"合并为训练集，输入学习器计算效用函数，通过遗传算法找到令效用函数最大的"附加变量"的合成方式。测试表明"银行存管"，"ICP认证","加入协会"，"异常经营次数"四个变量合成的"附加变量"具有较好的效果。

## Split Dataset

​	本轮测试中数据集$X$分为三个"基础变量"$X_{base}$与一个"附加变量"$X_{add}$。假设剔除三个基础变量后剩余变量集合$\{x_1,x_2,x_3,...,x_m\}$，"附加变量"$X_{add}$可表示为：
$$
X_{add} = \sum_{t=1}^{s}\omega_{t}x_t，1<t<m
$$
其中$\omega_{t}$是剩余变量$x_{t}​$的权重。本轮测试中“附加变量”由"银行存管"，"ICP认证","加入协会"，"异常经营次数"四个变量加权形成。

## Utility Function

​	本轮测试中，效用函数是机器学习算法的预测准确率。给定$m$维测试集$x$与二分类学习器$f(x)$$（f(x)\in\{0,1\}）$，效用函数的形式为：
$$
Utility = 1-\frac{\sum_{i=1}^{N}|f(x_i)-y_i|}{N}
$$
其中$N$是测试集包含的样本数量，$y_i\in\{0,1\}$是$x_i​$对应的预测结果。

​	以逻辑回归为例，效用函数可以表示为：
$$
\begin{cases}
Utility=1-\frac{\sum_{i=1}^{N}|round(\frac{1}{1+e^{\theta_0+\theta_1X_{base,i}+\theta_2X_{add,i}}})-y_{i}|}{N}\\
\\
X_{base}=(x_{实际资本}^T,x_{参考利率}^T,x_{经营时间}^T)\\
\\
X_{add}=\frac{1}{4}\sum_{m=1}^{4}\omega_{m}x_{m}\\
\\
x_m\in\{x_{银行存管}^T,x_{ICP认证}^T,x_{加入协会}^T,x_{异常经营次数}^T\}

\end{cases}
$$


## Result

​	本轮测试以随机森林为学习器（参数：n_esimators=5,max_depth=4），遗传算法的population size为100，染色体维数dim为4，最大迭代次数为160次。经过九次重复试验获得效用函数的均值、标准差、最大值，如下所示：

![img1](C:\Users\Administrator\Desktop\网贷plot\GAs\img1.png)

![img2](C:\Users\Administrator\Desktop\网贷plot\GAs\img2.png)

![img3](C:\Users\Administrator\Desktop\网贷plot\GAs\img3.png)

![img4](C:\Users\Administrator\Desktop\网贷plot\GAs\img4.png)

![img5](C:\Users\Administrator\Desktop\网贷plot\GAs\img5.png)

![img6](C:\Users\Administrator\Desktop\网贷plot\GAs\img6.png)

![img7](C:\Users\Administrator\Desktop\网贷plot\GAs\img7.png)

![img8](C:\Users\Administrator\Desktop\网贷plot\GAs\img8.png)

![img9](C:\Users\Administrator\Desktop\网贷plot\GAs\img9.png)

结果表明算法在多数情况下可以收敛，但有时仍然会陷入局部最优。通过遗传算法优化“附加变量”的合成方式，效用函数的均值平均提升0.7%，最高可达82.54%。

​	此外本文跟踪了第九次试验中每次迭代的效用函数分布，结果如下：

![效用函数分布2](C:\Users\Administrator\Desktop\网贷plot\GAs\效用函数分布2.png)

​	四项权重的变化曲线与最终结果如下所示（weight1到weight4分别代表"银行存管"，"加入协会"，"ICP认证","异常经营次数"），结果表明银行存管与ICP认证具有较高的权重

![权重变化曲线](C:\Users\Administrator\Desktop\网贷plot\GAs\权重变化曲线.png)

![最终权重](C:\Users\Administrator\Desktop\网贷plot\GAs\最终权重.png)

