import pandas as pd

#######################################################
#For CP 

cp = pd.read_csv("C:/Users/nathb/Downloads/new bot flow/new_NLEM_cellingprice (1).csv")

cp.rename(columns={'Celling_price': 'Ceiling_price'}, inplace=True)

def format_information(row):
    return f"The Formulation {row['Compositions']} is Scheduled under NLEM. The Strength of this drug is {row['Strength']}. The Dosage Form is {row['Dosage']}. The Ceiling Price is {row['Ceiling_price']}."

cp['Information'] = cp.apply(format_information, axis=1)

cp['Information'] = cp['Information'].astype(str)

cp['Input'] = cp['Compositions'] + ' ' + cp['Strength'] + ' ' + cp['Dosage']

cp.rename(columns={'Information': 'Response'}, inplace=True)

cp = cp.loc[:, ['Input', 'Response']]

cp.dropna(inplace=True)

cp['Input'] = cp['Input'].astype(str)

cp['text'] = cp.apply(lambda row: f"Below is an instruction that describes a task. Write a response that appropriately completes the request. ###Human:\nIs {row['Input']} scheduled?\n\n###Assistant:\n{row['Response']}", axis=1)

#########################################

#For NS

ns = pd.read_csv("C:/Users/nathb/Downloads/new bot flow/pharmatrack_non-scheduled (1).csv")

def format_information(row):
    return f"The Formulation {row['Compositions']} is Non-Scheduled under NLEM. The Strength of this drug is {row['Strength']}. The Dosage Form is {row['Dosage']}. The PTR is {row['PTR']}. "

ns['Response'] = ns.apply(format_information, axis=1)

ns['Response'] = ns['Response'].astype(str)

ns['Input'] = ns['Compositions'] + ' ' + ns['Strength'] + ' ' + ns['Dosage']


ns = ns.loc[:, ['Input', 'Response']]

ns.dropna(inplace=True)

ns['Input'] = ns['Input'].astype(str)

ns['text'] = ns.apply(lambda row: f"Below is an instruction that describes a task. Write a response that appropriately completes the request. ###Human:\nIs {row['Input']} scheduled?\n\n###Assistant:\n{row['Response']}", axis=1)

new_data = pd.concat([cp, ns], ignore_index=True)

new_data.to_csv("new_data.csv")


import pandas as pd

# Create the 'Input' column
cp['Input'] = cp['Compositions'].fillna('') + ' ' + cp['Strength'].fillna('') + ' ' + cp['Dosage'].fillna('')


# Create the 'Details' column
cp['Details'] = cp.apply(lambda row: [{'Composition': row['Compositions'], 
                                           'Strength': row['Strength'], 
                                           'Dosage': row['Dosage'], 
                                           'NLEM 2022': 'Scheduled',
                                           'Ceiling_price': row['Ceiling_price']}], axis=1)

# Select only the 'Input' and 'Details' columns
new_cp = cp[['Input', 'Details']]

# Write the result to a new CSV file
new_cp.to_csv("cp_transformed_data.csv", index=False)



# Create the 'Input' column
ns['Input'] = ns['Compositions'].fillna('') + ' ' + ns['Strength'].fillna('') + ' ' + ns['Dosage'].fillna('')

# Create the 'Details' column
ns['Details'] = ns.apply(lambda row: [{'Compositions': row['Compositions'], 
                                           'Strength': row['Strength'], 
                                           'Dosage': row['Dosage'], 
                                           'NLEM 2022': 'Non-Scheduled',
                                           'PTR': row['PTR'],
                                           'MRP': row['MRP']}], axis=1)

# Select only the 'Input' and 'Details' columns
new_ns = ns[['Input', 'Details']]

# Write the result to a new CSV file
ns.to_csv("transformed_data.csv", index=False)


transformed_data = pd.concat([new_cp, new_ns])

transformed_data.to_csv("transformed_data.csv") 


data= transformed_data.sample(n=2000, random_state=1)


import pandas as pd

# Assuming 'data' is your DataFrame
n_total = len(transformed_data)  # total number of rows in the DataFrame

# Calculate the number of rows for each part
n_top = int(n_total * 0.6)  # 60% of the total
n_bottom = n_total - n_top  # the rest

# Select the top 60% of the rows
top_data = data.iloc[:n_top]

# Select the bottom 40% of the rows
bottom_data = data.iloc[-n_bottom:]

# Concatenate the two parts to get your final DataFrame
final_data = pd.concat([top_data, bottom_data])

# If you want to shuffle the final data
final_data = final_data.sample(frac=1, random_state=1).reset_index(drop=True)


