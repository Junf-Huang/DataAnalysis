# Create random data with numpy
import numpy as np
import pandas as pd
import re
from snownlp import SnowNLP
import jieba
import jieba.analyse
from wordcloud import WordCloud
from matplotlib import pyplot as plt 

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='Junf-Huang', api_key='UcLG1VBERu4MiPHw7wXp')

string = ['好看,超长,拍照,上网,前买,照着,教训,翻新,割手,组装,算是,设定,发成,超快,买非,满意哦,超给,上能,扩音,晕死,']
#典型意见词云图
font = '/usr/share/fonts/adobe-source-han-sans/SourceHanSansCN-Regular.otf'
wc = WordCloud(font_path=font, #如果是中文必须要添加这个，否则会显示成框框
               background_color='white',
               width=1000,
               height=800,
               ).generate(string[0])
wc.to_file('word.png') #保存图片
plt.imshow(wc)  #用plt显示图片
plt.axis('off') #不显示坐标轴
plt.show() #显示图片
 



        

