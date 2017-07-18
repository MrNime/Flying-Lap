import pandas as pd

#make dataframe
df = pd.read_csv('Flying Lap\static\countries.csv')
# print (df.get_value(1,'Nationality'))

#set index to country name
df.set_index(['Country'], inplace = True)

#make code column lowercase
df['Code'] = df['Code'].str.lower()

#example usage
# fincode = df.loc[df['Nationality'] == 'Spanish','Code']
# print(fincode[0])

def nationality_to_code(nationality):
    """
    function to look up country code corresponding to
    the nationality.
    """
    codeseries = df.loc[df['Nationality'] == nationality, 'Code']
    return codeseries[0]
