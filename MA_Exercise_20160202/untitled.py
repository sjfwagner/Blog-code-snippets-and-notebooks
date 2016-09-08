import pandas as pd
import re
import string
import seaborn as sns
import numpy as np
from scipy import stats


from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.layouts import row, column
from bokeh.models.layouts import Spacer
from bokeh.models import ColumnDataSource, HoverTool,PanTool,WheelZoomTool,ResetTool,BoxZoomTool,Div,FixedTicker,FuncTickFormatter
#http://bokeh.pydata.org/en/latest/docs/user_guide/styling.html#functickformatter
import bokeh.models.widgets as widgets
from bokeh.charts import Scatter, defaults
from bokeh.io import curdoc
#from bokeh.chart import defaults



from datetime import timedelta

alpha = string.ascii_uppercase
def time_to_seconds(i,seconds=True): 
    i = filter(lambda x: x.isalpha() == False, i)
    i.strip()
    times = str(i).split(":")
    #  print times
    if len(times) == 2: 
        time = timedelta(minutes=int(times[0]),seconds=int(times[1]))
    if len(times) ==3: 
        time = timedelta(hours=int(times[0]),minutes=int(times[1]),seconds=int(times[2]))
    if seconds: 
        return time.total_seconds()
    return time

def seconds_formatted(seconds):
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%s:%s:%s" % (h, m, s)




females = pd.DataFrame().from_csv('MA_Exer_PikesPeak_Females.txt',sep='\t', index_col=None)
females['Gender'] = 'Female'
males = pd.DataFrame().from_csv('MA_Exer_PikesPeak_Males.txt',sep="\t",index_col=None)
males['Gender'] = 'Male'
dfs = [females,males]

for df in dfs: 
    #df[df['Hometown'] == 'Silver Spring M']['Hometown'] = 'Silver Spring MD'#['Net Tim'] = map(lambda i: i.replace('D','').strip(),)
    
    #df['Net Tim'] = map(lambda i: i.replace('D','').strip(), df['Net Tim'])
    df['Net Tim']= map(lambda i: i.translate(None,"*#"),df['Net Tim'])
    df['Div'] = map(lambda i: str(i).split('/')[0],df['Div/Tot'])
    #df['Net Tim'] = map(time_to_seconds,df['Net Tim'])
    df['Net_Seconds'] = map(lambda i: time_to_seconds(i),df['Net Tim'])
    df['Gun_Seconds'] = map(lambda i: time_to_seconds(i),df['Gun Tim'])

    #df['Net Tim']= map(lambda i: if (str(i).split(':')),df['Div/Tot'])
together = pd.concat(dfs)

gun_color_women ="#ff3399"
gun_color_men ='#0000ff'
net_color_women ="#9900cc"
net_color_men = "#006666"


####PLOT ONE#### DATA DISTRIBUTIONS - GUN TIME

plot_one = figure(plot_width=800,plot_height=600)
plot_one.xaxis.formatter = FuncTickFormatter.from_py_func(seconds_formatted)

#WOMEN
density = stats.kde.gaussian_kde(females['Gun_Seconds'].dropna())
x = np.arange(0.,max(females['Gun_Seconds'].dropna()), 1)
y = [density(y) for y in x]


plot_one.line(x,y,alpha=.7,color="#ff3399",legend="Women, Gun Time")

mean = females['Gun_Seconds'].mean()
plot_one.circle(mean,density(mean),color="#ff3399", legend="Women, Gun Time, Mean")

median = females['Gun_Seconds'].median()
plot_one.triangle(median,density(median),color="#ff3399", legend="Women, Gun Time, Median")

mode = females['Gun_Seconds'].mode()
#mode = mode.mean()
for i in mode: 
     plot_one.square(i,density(i),color="#ff3399", legend="Women, Gun Time, Mode")

#MEN
density = stats.kde.gaussian_kde(males['Gun_Seconds'].dropna())
x = np.arange(0.,max(males['Gun_Seconds'].dropna()), 1)
y = [density(y) for y in x]


plot_one.line(x,y,alpha=.7,color='#0000ff',legend="Men, Gun Time")

mean = males['Gun_Seconds'].mean()
plot_one.circle(mean,density(mean),color='#0000ff', legend="Men, Gun Time, Mean")

median = males['Gun_Seconds'].median()
plot_one.triangle(median,density(median),color='#0000ff', legend="Men, Gun Time, Median")

mode = males['Gun_Seconds'].mode()
#mode = mode.mean()
for i in mode: 
     plot_one.square(i,density(i),color='#0000ff', legend="Men, Gun Time, Mode")



### DATA DISTRIBUTIONS - NET TIME



#WOMEN
density = stats.kde.gaussian_kde(females['Net_Seconds'].dropna())
x = np.arange(0.,max(females['Net_Seconds'].dropna()), 1)
y = [density(y) for y in x]

####ax.plot(x, density(x),alpha=.3,color='#9900cc')

plot_one.line(x,y,alpha=.7,color="#9900cc",legend="Women, Net Time")

mean = females['Net_Seconds'].mean()
plot_one.circle(mean,density(mean),color="#9900cc", legend="Women, Net Time, Mean")

median = females['Net_Seconds'].median()
plot_one.triangle(median,density(median),color="#9900cc", legend="Women, Net Time, Median")

mode = females['Net_Seconds'].mode()
#mode = mode.mean()
for i in mode: 
     plot_one.square(i,density(i),color="#9900cc", legend="Women, Net Time, Mode")

#MEN
density = stats.kde.gaussian_kde(males['Net_Seconds'].dropna())
x = np.arange(0.,max(males['Net_Seconds'].dropna()), 1)
y = [density(y) for y in x]
####ax.plot(x, density(x),alpha=.3,color='#ff3399')

plot_one.line(x,y,alpha=.7,color='#006666',legend="Men, Net Time")

mean = males['Net_Seconds'].mean()
plot_one.circle(mean,density(mean),color='#006666', legend="Men, Net Time, Mean")

median = males['Net_Seconds'].median()
plot_one.triangle(median,density(median),color='#006666', legend="Men, Net Time, Median")

mode = males['Net_Seconds'].mode()
#mode = mode.mean()
for i in mode: 
     plot_one.square(i,density(i),color='#006666', legend="Men, Net Time, Mode")
