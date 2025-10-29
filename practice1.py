import pandas as pd

students_data = {
    'Name': ['Anna', 'Ben', 'Cara', 'Drew', 'Ella'],
    'Age': [20,21,22,20,23],
    'Grade':[89, 75, 92, 85, 90],
    'City': ['Manila', 'Cebu', 'Davao', 'Manila', 'Baguio'],
    'Scholarship': ['Yes', 'No', 'Yes', 'No', 'Yes']
}

students_df = pd.DataFrame(students_data)

students_df.set_index('Name', inplace=True)
row = students_df.iloc[3]

print(row)