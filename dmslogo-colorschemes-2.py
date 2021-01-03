df = (df
      .assign(color=lambda x: x['value'].map(map1.val_to_color),
              color2=lambda x: x['value'].map(map2.val_to_color),
              )
      )
df
# value    color   color2
# 0      0  #440154  #00224d
# 1      1  #30678d  #575d6d
# 2      2  #35b778  #a59b73
# 3      1  #30678d  #575d6d
# 4      3  #fde724  #fde737
# 5      0  #440154  #00224d
