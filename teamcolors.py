import pandas as pd

#make dataframe
# df = pd.read_csv('team_kleuren.csv')
df = pd.read_csv('team_kleuren.csv', index_col = [0,1])
# print (df.get_value(1,'Nationality'))

#set index to country name
# df.set_index(['name'], inplace = True)

#example usage
# # hexkleur = df.loc[df['constructorId'] == 'mercedes','Hex']
# # print(hexkleur[0])
# print(df)
# hexkleur = df.loc[df['constructorId'] == 'mercedes','Hex'][2016]
# print(hexkleur[0])


def constructor_id_to_hex(constructor_id, year):
    """
    function to look up hex color-code corresponding to
    the constructor_id.
    """
    hexseries = df.loc[df['constructorId'] == constructor_id, 'Hex'][year]
    return hexseries[0]

# print(constructor_id_to_hex('manor', 2016))
