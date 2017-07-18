import pandas as pd

#make dataframe
df = pd.read_csv('static\\team_kleuren.csv')
# print (df.get_value(1,'Nationality'))

#set index to country name
df.set_index(['name'], inplace = True)

#example usage
# hexkleur = df.loc[df['constructorId'] == 'mercedes','Hex']
# print(hexkleur[0])

def constructor_id_to_hex(constructor_id):
    """
    function to look up hex color-code corresponding to
    the constructor_id.
    """
    hexseries = df.loc[df['constructorId'] == constructor_id, 'Hex']
    return hexseries[0]
