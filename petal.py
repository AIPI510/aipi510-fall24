import seaborn as sns
from test import *

# load data
data = sns.load_dataset('iris') 

# mutate data to get largest average petal length
data = data.groupby(['species']).mean().sort_values('petal_length', ascending=False)
data = data.loc[:,'petal_length'].head(1)

# test data manipulations
test_length(data)
test_type(data)

# show largest average petal length
print(data)

