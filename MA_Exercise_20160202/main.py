import pandas as pd
import re
import string
import numpy as np
from scipy import stats


from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.layouts import row, column
from bokeh.models.layouts import Spacer
from bokeh.models import ColumnDataSource, HoverTool,PanTool,WheelZoomTool,ResetTool,BoxZoomTool,Div,FixedTicker,FuncTickFormatter
import bokeh.models.widgets as widgets
from bokeh.charts import Scatter, defaults
from bokeh.io import curdoc
from bokeh.palettes import plasma
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.charts import Scatter



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
    df['Pace'] = map(lambda i: time_to_seconds(i),df['Pace'])

    #df['Net Tim']= map(lambda i: if (str(i).split(':')),df['Div/Tot'])
together = pd.concat(dfs)
together['Rank'] = together['Net_Seconds'].rank()
gun_color_women ="#ff3399"
gun_color_men ='#0000ff'
net_color_women ="#9900cc"
net_color_men = "#006666"


####PLOT ONE#### DATA DISTRIBUTIONS - GUN TIME

plot_one = figure(plot_width=900,plot_height=500)
plot_one.xaxis.formatter = FuncTickFormatter.from_py_func(seconds_formatted)
#hover_one =HoverTool(
#        tooltips=[
#            ("index", "$index"),
#            ("(x,y)", "($x, $y)"),
#            ("desc", "@desc"),
#        ]
#    )


plot_one.add_tools(HoverTool())
#WOMEN
density = stats.kde.gaussian_kde(females['Gun_Seconds'].dropna())
x = np.arange(0.,max(females['Gun_Seconds'].dropna()), 1)
y = [density(y) for y in x]


plot_one.line(x,y,alpha=.4,color="#ff3399",legend="Women, Gun Time", line_width=5)

mean = females['Gun_Seconds'].mean()
plot_one.circle(mean,density(mean),color="#ff3399", legend="Women, Gun Time, Mean",size=10)

median = females['Gun_Seconds'].median()
plot_one.triangle(median,density(median),color="#ff3399", legend="Women, Gun Time, Median",size=10)

mode = females['Gun_Seconds'].mode()
#mode = mode.mean()
for i in mode: 
     plot_one.square(i,density(i),color="#ff3399", legend="Women, Gun Time, Mode",size=10)

#MEN
density = stats.kde.gaussian_kde(males['Gun_Seconds'].dropna())
x = np.arange(0.,max(males['Gun_Seconds'].dropna()), 1)
y = [density(y) for y in x]


plot_one.line(x,y,alpha=.4,color='#0000ff',legend="Men, Gun Time", line_width=5)

mean = males['Gun_Seconds'].mean()
plot_one.circle(mean,density(mean),color='#0000ff', legend="Men, Gun Time, Mean",size=10)

median = males['Gun_Seconds'].median()
plot_one.triangle(median,density(median),color='#0000ff', legend="Men, Gun Time, Median",size=10)

mode = males['Gun_Seconds'].mode()
#mode = mode.mean()
for i in mode: 
     plot_one.square(i,density(i),color='#0000ff', legend="Men, Gun Time, Mode",size=10)



### DATA DISTRIBUTIONS - NET TIME



#WOMEN
density = stats.kde.gaussian_kde(females['Net_Seconds'].dropna())
x = np.arange(0.,max(females['Net_Seconds'].dropna()), 1)
y = [density(y) for y in x]

####ax.plot(x, density(x),alpha=.3,color='#9900cc')
plot_one.xaxis.axis_label = 'Time'
plot_one.yaxis.axis_label = 'Data Density'
plot_one.line(x,y,alpha=.4,color="#9900cc",legend="Women, Net Time", line_width=5)

mean = females['Net_Seconds'].mean()
plot_one.circle(mean,density(mean),color="#9900cc", legend="Women, Net Time, Mean",size=10)

median = females['Net_Seconds'].median()
plot_one.triangle(median,density(median),color="#9900cc", legend="Women, Net Time, Median",size=10)

mode = females['Net_Seconds'].mode()
#mode = mode.mean()
for i in mode: 
     plot_one.square(i,density(i),color="#9900cc", legend="Women, Net Time, Mode",size=10)

#MEN
density = stats.kde.gaussian_kde(males['Net_Seconds'].dropna())
x = np.arange(0.,max(males['Net_Seconds'].dropna()), 1)
y = [density(y) for y in x]
####ax.plot(x, density(x),alpha=.3,color='#ff3399')

plot_one.line(x,y,alpha=.4,color='#006666',legend="Men, Net Time", line_width=5)

mean = males['Net_Seconds'].mean()
plot_one.circle(mean,density(mean),color='#006666', legend="Men, Net Time, Mean",size=10)

median = males['Net_Seconds'].median()
plot_one.triangle(median,density(median),color='#006666', legend="Men, Net Time, Median",size=10)

mode = males['Net_Seconds'].mode()
#mode = mode.mean()
for i in mode: 
     plot_one.square(i,density(i),color='#006666', legend="Men, Net Time, Mode",size=10)


####PLOT TWO#### GUN VS NET TIME - HEAD TO HEAD

plot_two = figure(plot_width=450,plot_height=375)
plot_two.xaxis.formatter = FuncTickFormatter.from_py_func(seconds_formatted)
plot_two.yaxis.formatter = FuncTickFormatter.from_py_func(seconds_formatted)
plot_two.xaxis.axis_label = 'Gun Time'
plot_two.yaxis.axis_label = 'Net Seconds'

plot_two.triangle(females['Gun_Seconds'],females['Net_Seconds'],color="#ff3399",legend = "Women",alpha=.3,size=10)
plot_two.square(males['Gun_Seconds'],males['Net_Seconds'],color='#0000ff',legend="Men",alpha=.3,size=10)

####PLOT THREE#### GUN VS NET TIME - DIFF


together['Net_Gun_Diff'] = together['Gun_Seconds'] - together['Net_Seconds']


plot_three = figure(plot_width=450,plot_height=375)
plot_three .xaxis.formatter = FuncTickFormatter.from_py_func(seconds_formatted)
plot_three.xaxis.axis_label = 'Gun Time'
plot_three.yaxis.axis_label = 'Difference between Gun Time and Net Time'

plot_three .triangle(together[together['Gender']=='Female']['Gun_Seconds'],
			together[together['Gender']=='Female']['Net_Gun_Diff'],
			color="#ff3399",
			legend = "Women",alpha=.3,
			size=10)
plot_three .square(together[together['Gender']=='Male']['Gun_Seconds'],
			together[together['Gender']=='Male']['Net_Gun_Diff'],
			color='#0000ff',legend="Men",alpha=.3
			,size=10)

####PLOT FIVE#### COMPARE DIVISIONS WOMEN

plot_five = figure(plot_width=425,plot_height=400)

#plot_five = Scatter(females, x='Net_Seconds', y='Pace', color='Div',
#            title="Net Seconds v. Pace, colored by Division", legend="top_left",
#            xlabel="Net Seconds", ylabel="Pace",plot_width=900,plot_height=500)
plot_five.xaxis.formatter = FuncTickFormatter.from_py_func(seconds_formatted)
colors = dict(zip(set(females['Div']),plasma(len(set(females['Div'])))))
colorsm = dict(zip(set(males['Div']),plasma(len(set(males['Div'])))))
#print colors
plot_five.xaxis.axis_label = 'Net Seconds'
plot_five.yaxis.axis_label = 'Division'
plot_five.title = "Women by Divsion"
females['color'] = map(lambda i: colors[i], females['Div'])
#females['Rank'] = females['Net_Seconds'].rank()
plot_five.triangle(females['Net_Seconds'],females['Div'],color=females['color'],alpha=.3,size=10)
#plot_five.square(males['Div'],males['Place'],color='#0000ff',legend="Men",alpha=.3,size=10)

####PLOT Six#### COMPARE DIVISIONS MALE

plot_six = figure(plot_width=425,plot_height=400)
colors = dict(zip(set(males['Div']),plasma(len(set(males['Div'])))))
plot_six.title = "Men by Divsion"

plot_six.xaxis.axis_label = 'Net Seconds'
plot_six.yaxis.axis_label = 'Division'
plot_six.xaxis.formatter = FuncTickFormatter.from_py_func(seconds_formatted)
males['color'] = map(lambda i: colors[i], males['Div'])
#females['Rank'] = females['Net_Seconds'].rank()
plot_six.square(males['Net_Seconds'],males['Div'],color=males['color'],alpha=.3,size=10)
#plot_five.square(males['Div'],males['Place'],color='#0000ff',legend="Men",alpha=.3,size=10)


####PLOT FOUR#### WITHIN DIV COMPARISON
plot_four = figure(plot_width=600,plot_height=400)
plot_four.xaxis.formatter = FuncTickFormatter.from_py_func(seconds_formatted)
plot_four.yaxis.formatter = FuncTickFormatter.from_py_func(seconds_formatted)
plot_four.xaxis.axis_label = 'Gun Time'
plot_four.yaxis.axis_label = 'Net Time'

div_select = widgets.MultiSelect(title="Select Division", options = [str(i) for i in set(together['Div'])], value = ['108'], width = 30)
gender_select = widgets.MultiSelect(title="Select Gender", options = ['Male','Female'], value = ['Male'], width = 30)
runner_select = widgets.MultiSelect(title="Select Runner", options = [str(i) for i in set(together[(together['Div']==108) & (together['Gender'] == 'Male')]['Name'])], value = ['Chris Doe'], width = 50)

Comparison_Source = ColumnDataSource(data = dict(
						 gender = [],
						 name = [],
						 division = [],
						 gun_time = [],
						 net_time = [],
						 color = [],
						 pace = [],
						 ))
Text_Source = ColumnDataSource(data=dict(
							text = ['']))

def select_data(): 
	division = div_select.value
	gender = div_select.value
	runner = runner_select.value	
	data = together
	
	data = data[data['Div'].isin(div_select.value)]
	data = data[data['Gender'].isin(gender_select.value)]
	print len(data)
	#print
	#print runner
	#print 
	runner_time = list(data[data['Name'] == runner[0]]['Net_Seconds'])
	if len(runner_time) > 0:
		runner_time= runner_time[0]
		diff = float(data['Net_Seconds'].quantile(.1) - runner_time)
		if diff > 0: 
			text = "".join([runner[0] , ' is ' , str(diff) ,' seconds ahead of the top 10th percentile'])
		else: 
			text = "".join([runner[0] , ' is ' ,str(abs(diff)), ' seconds behind of the top 10th percentile'])
	else:
		text = 'Null'
	#print text
	return data,text

def update():
	df,text =  select_data()
	
	runner_select.options = [str(i) for i in set(df['Name'])]
	df['color'] = plasma(len(df['Name'])) 
	#df[df['Name'].isin(runner_select.value)]['color']='#ff6600'
	#print df
	Comparison_Source.data = dict(
					gender = df['Gender'],
					name = df['Name'],
					division = df['Div'],
					gun_time = df['Gun_Seconds'],
					net_time = df['Net_Seconds'],
					color = df['color'],
					pace = df['Pace']
					)
	Text_Source.data=dict(text=[text])


plot_four.text(x=3000,y=3000,text='text',source=Text_Source,text_font_size='10pt')
plot_four.circle(x='gun_time',y='net_time',color='color',size = 15,source=Comparison_Source)




hover_one =HoverTool(
        tooltips=[
            ("name", "@name"),
            ("gun time", "$x"),
            ("net time", "$y"),
        ]
    )
plot_four.add_tools(hover_one)



controls = [runner_select,gender_select,div_select]

for control in controls:
    control.on_change('value', lambda attr, old, new: update())

head= Div(text ="""<h1>Pike's Peak 10K</h1>
			 <h3>A survey of Race times</h3>
			 Sophie J.F. Wagner | sjfwagner@gmail.com 
			 <br><br><br>""")
head1 = Div(text="""<h2>The Distribution of the Data</h2>""")
d1= Div(text = """<h3>Overall runtimes were normally distributed.</h3><br>
			 The distributions of the data can be seen graphed at the left. Race Results, both net and gun times, for each gender is generally normally distributed, with close mean and medians. <br><br>
			 For women, the data skews to the right, indicating that overall women’s run times were slower. The greater density of the of slow times, skew the mode to the left. In this case the mode is not particularly informative, as times vary widely. The number of unique times is only marginally smaller than the number of participants, for both men and women there are roughly 75% of all times are unique. <br><br> 
			 For men, the data skews left, indicating that men run faster on average. The lower, more sloping peak also indicates that men’s finish times varied more than the women, instead of being strongly grouped around a single time men's finish times varied more.""")
head2 = Div(text="""<h2>Net Time v. Gun Time</h2>""")
d2= Div(text = """
			 <h3>Closely correlated, differences likely represent organizer intent</h3><br>
			 Net time measures the elapsed time of the runner, whereas gun time measures the elapsed time from the start of the race to the runner's finish.<br><br>
			 Net Time and Gun Time almost perfectly correlated - 99.5% - such that while the time may differ slightly, for the most part only a few seconds different, that difference is consistent for all times. The actual difference in seconds, between the gun time and net time shows the pattern to the left. Groups of men and women show a greater time. As the the gun time to complete the race grows, the difference also grows. This likely indicates that the divisions in the race were started in waves, giving the runners space between each other and lightening traffic on the course. 
""")
head3 = Div(text="""<h2>Difference within Divisions</h2>""")
d5= Div(text = """
			 <h3>Racetimes slow as divisions increase</h3><br>
			 Divisions within gender, show that among the top performers, division has verly little effect on the 
			 to differenciate the top performers, particularly in younger divisions. Higher Divisions, with older participants, have slower completion times.
			 <br><br>A linear model, on net time by division, controlling gender and Age, significantly explains roughly 50% of the variance in net time.""")
head4 = Div(text="""<h2>Differences Among Divisions</h2>""")
d4= Div(text = """
			 <h3>Exploring within Divisions</h3><br>
			 Divisions are divide racers into age and gender group. <br><br>
			 The graphic at the left allows you to explore the divisions, by plotting the Gun Time & Net Time of racers in the same division. 
			 <br> <br> The text at the bottom right will show how far from the top 10th percentile the specific racer fell. The names will update based on your selections.""")

row1 = row(*[plot_one,Spacer(width=30),d1])
row2 = row(*[plot_two,Spacer(width=30),d2,Spacer(width=30),plot_three])
subc = column(*[runner_select,gender_select,div_select])
row4 = row(*[d4,Spacer(width=70),subc,Spacer(width=70),plot_four])
row5 = row(*[plot_five,Spacer(width=30),plot_six,Spacer(width=30),d5])
column1 = column(*[head,head1,row1,head2,row2,head3,row4,head4, row5])

l = layout([[column1]])
update()

curdoc().add_root(l)
curdoc().title = "Test"