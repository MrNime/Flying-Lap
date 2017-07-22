import pandas as pd

#make dataframe
df = pd.read_csv('countries.csv')
# print (df.get_value(1,'Nationality'))

#set index to country num_code
df.set_index(['num_code'], inplace = True)

# make code column lowercase
df['alpha_2_code'] = df['alpha_2_code'].str.lower()

# #example usage
# code = df.loc[df['nationality'] == 'British','alpha_2_code']
# print(code.values[0])


def nationality_to_code(nationality):
    """
    function to look up country code corresponding to
    the nationality.
    """
    code = df.loc[df['nationality'] == nationality,'alpha_2_code']
    return code.values[0]
