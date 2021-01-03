import pandas as pd
from dmslogo.colorschemes import ValueToColorMap
# >>>
df = pd.DataFrame({'value': [0, 1, 2, 1, 3, 0]})
map1 = ValueToColorMap(df['value'].min(),
                       df['value'].max())
map2 = ValueToColorMap(df['value'].min(),
                       df['value'].max(),
                       cmap='cividis')
