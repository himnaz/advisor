import pandas as pd
import numpy as np
import os


def write_excel (output_fname,sheet_name,df):
 if os.path.exists(output_fname):
   with pd.ExcelWriter(output_fname, engine='openpyxl', mode='a',if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name=sheet_name, index=False)

 else:
   with pd.ExcelWriter(output_fname, engine='openpyxl', mode='w') as writer:
    df.to_excel(writer, sheet_name=sheet_name, index=False)


# Read the CSV files
d1 = pd.read_csv('c:\\documentation\\gdocs\\test0.csv')
d2 = pd.read_csv('c:\\documentation\\gdocs\\test1.csv')

# Process d1 - fill forward the target entity and target column values
d1_processed = d1.copy()
#d1_processed['target entity'] = d1_processed['target entity'].fillna(method='ffill')
#d1_processed['target column'] = d1_processed['target column'].fillna(method='ffill')

d1_processed['target entity'] = ''
d1_processed['target column'] = ''

# Select only the columns we want from d1
d1_columns = ['target entity', 'target column', 'population', 'target data type', 
              'source schema.table', 'source field', 'source data type', 
              'is pbi logic? (y/n)', 'snake_case']

# Rename derived requested attribute to column_name for joining
d1_processed = d1_processed[d1_columns].rename(columns={
    'snake_case': 'column_name'
})

# Join d1 and d2 on column_name
merged_df = pd.merge(
    d1_processed,
    d2[['column_name', 'column_type']],
    on='column_name',
    how='outer'
)

write_excel('c:\\documentation\\gdocs\\test2_out.xlsx','merged_df',merged_df)
# Create the final dataframe with the required structure
result_rows = []

# Process each unique target entity and target column combination from d1
unique_combinations = d1_processed[['target entity', 'target column']].drop_duplicates()
write_excel('c:\\documentation\\gdocs\\test2_out.xlsx','unique_combinations',unique_combinations)

for _, combo in unique_combinations.iterrows():
    target_entity = combo['target entity']
    target_column = combo['target column']
    
    # Get all rows for this combination
    combo_rows = d1_processed[(d1_processed['target entity'] == target_entity) & 
                              (d1_processed['target column'] == target_column)]
    
    # Add first row with target entity and column
    first_row = combo_rows.iloc[0]
    result_rows.append({
        'target entity': first_row['target entity'],
        'target column': first_row['target column'],
        'population': first_row['population'] if pd.notna(first_row['population']) else '',
        'target data type': first_row['target data type'] if pd.notna(first_row['target data type']) else '',
        'source schema.table': first_row['source schema.table'] if pd.notna(first_row['source schema.table']) else '',
        'source field': first_row['source field'] if pd.notna(first_row['source field']) else '',
        'source data type': first_row['source data type'] if pd.notna(first_row['source data type']) else '',
        'is pbi logic? (y/n)': first_row['is pbi logic? (y/n)'] if pd.notna(first_row['is pbi logic? (y/n)']) else ''
    })
    
    # Add subsequent rows with empty target entity and column
    for _, row in combo_rows.iloc[1:].iterrows():
        result_rows.append({
            'target entity': '',
            'target column': '',
            'population': '',
            'target data type': '',
            'source schema.table': row['source schema.table'] if pd.notna(row['source schema.table']) else '',
            'source field': row['source field'] if pd.notna(row['source field']) else '',
            'source data type': row['source data type'] if pd.notna(row['source data type']) else '',
            'is pbi logic? (y/n)': row['is pbi logic? (y/n)'] if pd.notna(row['is pbi logic? (y/n)']) else ''
        })

# Add address columns from d2 that are not in d1
d1_columns_set = set(d1_processed['column_name'].unique())
d2_columns = d2['column_name'].unique()

# Get address columns from d2 that are not in d1
new_columns = [col for col in d2_columns if col not in d1_columns_set]

# Add these columns to the result
for col in new_columns:
    col_type = d2[d2['column_name'] == col]['column_type'].iloc[0]
    result_rows.append({
        'target entity': 'address',
        'target column': col,
        'population': '',
        'target data type': col_type,
        'source schema.table': '',
        'source field': '',
        'source data type': '',
        'is pbi logic? (y/n)': ''
    })

# Create the final dataframe
final_df = pd.DataFrame(result_rows)

# Define the desired column order for sorting
desired_order = ['address_line_1', 'address_line_2', 'address_line_3', 
                 'address_line_4', 'address_line_5', 'country', 'postcode']

# Sort the dataframe
def get_sort_order(row):
    if row['target column'] in desired_order:
        return desired_order.index(row['target column'])
    return -1  # Put non-address columns first

# Sort and reset index
final_df['sort_key'] = final_df.apply(get_sort_order, axis=1)
final_df = final_df.sort_values(['sort_key', 'target column']).drop('sort_key', axis=1)
final_df = final_df.reset_index(drop=True)

# Fill NaN values with empty string
final_df = final_df.fillna('')

# Save to CSV
#final_df.to_csv('test2.csv', index=False)

write_excel('c:\\documentation\\gdocs\\test2_out.xlsx','out',final_df)

