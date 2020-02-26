import pandas as pd
import matplotlib as mp
import matplotlib.pyplot as plt


_9form = pd.read_excel('9form.xlsx', header = 1).drop(index=0)
_9form['Form'] = 9
_10form = pd.read_excel('10form.xlsx', header = 1).drop(index=0, columns = ['Unnamed: 5', 'Unnamed: 6', 'Район, місто', 'Місце'])
_10form['Form'] = 10
_11form = pd.read_excel('11form.xlsx', header = 1).drop(index=0)
_11form['Form'] = 11

df = pd.concat([_9form, _10form, _11form], ignore_index = True)

print('------------------------ 1 -----------------------')

# Creating a new DataFrame due to issue caused by different amount of whitespaces in the name of the same school (excel issue)
dff = df['Школа'].apply(lambda x: x.replace(' ',''))  
#print(dff.value_counts())

print('------------------------ 2 -----------------------')
pattern = '(Ужгород|Хуст|Мукачів|Сокирниць|Солотвин|Лисичівськ|Великораковець)'
df['Region'] = df['Школа'].str.extract(pattern)
participantsCount = df['Region'].value_counts()
participantsCount.plot(kind = 'bar')
#plt.show()

print('------------------------ 3 -----------------------')
# list(dict.fromkeys(df['Form'].values))           # Get all column Form values without duplicates using Python
# df.drop_duplicates('Form')['Form'].values        # Get all column Form values without duplicates using Pandas methods
df['Diploma degree'] = 'None'
for form in df.drop_duplicates('Form')['Form'].values:
    index = df.loc[df['Form']==form].index[0]
    df.iloc[index,-1] = 'I'
    df.iloc[index+1:index+3,-1] = 'II'
    df.iloc[index+3:index+6,-1] = 'III'
#print(df)

print('------------------------ 4 -----------------------')
df['Winner'] = False
for form in df.drop_duplicates('Form')['Form'].values:
    index = df.loc[df['Form']==form].index[0]
    df.iloc[index:index+3,-1] = True
#print(df.loc[df['Winner']==True]['Region'].value_counts())

print('------------------------ 5 -----------------------')
countPercentage = dict()
for city in df.drop_duplicates('Region')['Region'].values:
    countPercentage[city] = "%.2f" % (len(df.loc[(df['Winner'] == True) & (df['Region'] == city)]['Region'].index) / len(df.loc[df['Region']==city]['Region'].index) * 100) + '%'
# print(countPercentage)


print('------------------------ 6 -----------------------')

#  40    10    30    30

# ----------------------------- Method 1 -------------------------------------
data = {'Form':df.drop_duplicates('Form')['Form'].values, 'Task 1':[], 'Task 2':[], 'Task 3':[],'Task 4':[]}    

for form in df.drop_duplicates('Form')['Form'].values:
        data['Task 1'].append("%.2f" % (df.loc[df['Form']==form]['К-сть балів'].sum()/df.loc[df['Form']==form]['Form'].size/40*100) +'%')
        data['Task 2'].append("%.2f" % (df.loc[df['Form']==form]['Unnamed: 2'].sum()/df.loc[df['Form']==form]['Form'].size/10*100) +'%')
        data['Task 3'].append("%.2f" % (df.loc[df['Form']==form]['Unnamed: 3'].sum()/df.loc[df['Form']==form]['Form'].size/30*100) +'%')
        data['Task 4'].append("%.2f" % (df.loc[df['Form']==form]['Unnamed: 4'].sum()/df.loc[df['Form']==form]['Form'].size/30*100) +'%')
        
results = pd.DataFrame(data)
print(results)

# ----------------------------- Method 2 -------------------------------------
data = {'Form':df.drop_duplicates('Form')['Form'].values}
results = pd.DataFrame(data)

for y in range(1,5):
    if y == 1:
        div = 40
    elif y == 2:
        div = 10
    elif y == 3:
        div = 30
    else:
        div = 30
    results[f'Task {y}'] = df.groupby('Form').mean().iloc[: , y].apply(lambda x: "%.2f" % (x/div*100) + '%').values

print(results)

# ---------------------------- Method 3 (Actually Method 2 is based on this one xD) -------------
data = {'Form':df.drop_duplicates('Form')['Form'].values}
results = pd.DataFrame(data)

results['Task 1'] = df.groupby('Form').mean().iloc[: , 1].apply(lambda x: "%.2f" % (x/40*100) + '%').values
results['Task 2'] = df.groupby('Form').mean().iloc[: , 2].apply(lambda x: "%.2f" % (x/10*100) + '%').values
results['Task 3'] = df.groupby('Form').mean().iloc[: , 3].apply(lambda x: "%.2f" % (x/30*100) + '%').values
results['Task 4'] = df.groupby('Form').mean().iloc[: , 4].apply(lambda x: "%.2f" % (x/30*100) + '%').values

print(results)
# ------------------------------------------------------------------------------------------------

results['Hardest Task'] =  [ f'Task {str(list(x).index(x.min())+1)} - {x.min()}' for x in results.iloc[ : , 1:5].values]
print(results)







#  first three
# print(_9form.head(3))

# last three
# print(_11form.tail(2))

# names of each column
# print(_10form.columns)

# specific column(list if columns) + slice
# print(_11form[['Школа',"К-сть балів"]][0:5])

# get row (use id1 : id2 to get rows) by ID (using integer location ( df.iloc[] ))
# print(_10form.iloc[3:6])

# get access to each row
# for index, row in _10form.iterrows():
#   print(index, row[8])

# get rows that satisfies condition (using df.loc[ condition ] )
# print(_10form.loc[_10form['К-сть балів']<26])

# read specific location ( df.iloc[id of the row , id of the column])
# print(_10form.iloc[2,8])


# not really useful method
# print(_10form.describe())

# sort values by column ( df.sort_values( [column name, column name] , *ascending = False ( [1,0] True - for first column, False - for second )* ) )
# print(_10form.sort_values('Школа'))

# create a new column based on values of existed (not really good method)
#_10form['Sum'] = _10form['К-сть балів'] + _10form['Unnamed: 2']
#print(_10form)

# create a new column based on values of existed (really good method)
#_10form['Sum'] = _10form.iloc[ : , 1:3].sum(axis=1)     axis = 1 means adding horizontally
#print(_10form)

# remove the specific column/row ( df = df.drop(column/row = name/index))
# _10form = _10form.drop(columns = 'Sum')
# print(_10form)

# change the columns position (e.g. we want the llast column be the fourth)
# cols = list(_10form.columns.values)
# _10form = _10form[cols[0:3] +  [ cols[-1] ] + cols[3:-1]]


# change the name of values (e.g. None to Participant)

# df.loc[ df['Diploma degree'] == 'None', 'Diploma degree' ] = 'Participant'
# print(df)

