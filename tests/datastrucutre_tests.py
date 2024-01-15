import pandas as pd

# Test 1 - proving words are ordered and can return in the way they were added
#    (to maintain the order they were retrieved from SS)

# Example data
data = {
    'word': ['word1', 'word1', 'word1', 'word2', 'word2'],
    'type': ['noun', 'adjective', 'verb', 'noun', 'verb'],
    'definition': ['def1', 'def2', 'def3', 'def4', 'def5'],
    'example': ['ex1', 'ex2', 'ex3', 'ex4', 'ex5']
}

# Creating a DataFrame
df = pd.DataFrame(data)

# Grouping by 'word'
grouped_df = df.groupby('word')

# Iterating through groups and printing definitions
for word, group in grouped_df:
    print(f"Definitions for {word}:")
    for index, row in group.iterrows():
        print(f"  Type: {row['type']}, Definition: {row['definition']}, Example: {row['example']}")
    print()


# Test 2 - creating and visualizing convenient data storage

# Example data
data2 = { 
    'Word': ['juzgar'],
    'Translation': ['to judge'],
    'type':['transitive verb'],
    'Details': [ #TODO: come up with better word for "Details"??
        {'Subdefinitions': [
            {'Subdef': '1. legal', 'Subtrans': 'a. to judge', 'Example': 'el juez...'},
            {'Subdef': '1. legal', 'Subtrans': 'b. to try', 'Example': 'no te pueden juzgar...'},
            {'Subdef': '2. to form an opinion about', 'Subtrans': 'a. to judge', 'Example': 'no deberías...'}
        ]}
    ]
}


# Creating a DataFrame
df2 = pd.DataFrame(data2)

df_exploded = df2.explode('Details')

normalized = pd.json_normalize(df2['Details'])

# Concatenate the 'Details' column with the DataFrame
df_result = pd.concat([df2[['Word', 'Translation','type']], normalized.explode('Subdefinitions')], axis=1)

print(df_result)