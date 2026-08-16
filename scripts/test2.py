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
d11 = pd.read_csv('c:\\documentation\\gdocs\\test0.csv')
d22 = pd.read_csv('c:\\documentation\\gdocs\\test1.csv')

def populate_table_specific_attribute_df(d1,d2):
    d2['row_number'] = d2.reset_index().index

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
        d2[['database_name','table_name','column_name', 'column_type','pk','row_number']],
        on='column_name',
        how='outer'
    )

    write_excel('c:\\documentation\\gdocs\\test2_out.xlsx','merged_df',merged_df)


    ######################

    col_list = []
    prev_attribute = ''
    #curr_attribute = ''
    first_row = True
    for index, row in merged_df.iterrows():
    #print(row)
    
     if first_row:  #The first row in the iteration
        row['target database'] = row['database_name']
        row['target entity'] = row['table_name']
        row['target column'] = row['column_name']
        row['target data type'] = row['column_type']
        row['PK? (Y/N)'] = row['pk']
        row['Nullable? (Y/N)'] = ''
        prev_attribute = row['column_name']
        #curr_attribute = row['column_name']
        first_row = False

     elif prev_attribute != row['column_name']:
        row['target database'] = row['database_name']
        row['target entity'] = row['table_name']
        row['target column'] = row['column_name']
        row['target data type'] = row['column_type']
        row['PK? (Y/N)'] = row['pk']
        row['Nullable? (Y/N)'] = ''
        prev_attribute = row['column_name']

     col_list.append(row)


    final_df = pd.DataFrame(col_list)
    final_df = final_df.drop(['database_name', 'table_name', 'column_name','column_type','pk'], axis=1)
    final_df = final_df.fillna('')
    final_df = final_df[['target database', 'target entity', 'target column', 'target data type','PK? (Y/N)','Nullable? (Y/N)','source schema.table','source field','source data type','is pbi logic? (y/n)']]
    return final_df

write_excel('c:\\documentation\\gdocs\\test2_out.xlsx','out',populate_table_specific_attribute_df(d11,d22))

