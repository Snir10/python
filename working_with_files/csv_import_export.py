import pandas as pd
import csv



print("\n*************** CSV IMPORT\EXPORT APP ****************\n")

csv_data = pd.read_csv(r'C:\pics\db.csv')
df = pd.DataFrame(csv_data, columns=['name', 'age', 'email', 'test_grade', 'time', 'test_type'])
print(df)

# Iterate Over Dataframe Data (CSV Data)
for index, row in df.iterrows():
    print(row['name'], row['age'])



print('starting write on CSV')

# Create and Open new CSV file.
with open('new_db.csv', 'w') as file:
    writer = csv.writer(file)

#  Manipulate Data
csv_data["split by 10"] = csv_data["age"] / 10
csv_data["concatenate email plus name"] = csv_data["email"] + " " + csv_data["name"] + " just a basic STR"


# Export Data object to actual CSV
csv_data.to_csv("C:\\pics\\new_csv_data.csv")
print('done')


