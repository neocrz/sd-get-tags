import pandas as pd
import os
import re

# Define the CSV file path for the dataset
dataset_file = 'tag_dataset.csv'

whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ,')

# Create a new dataset if it doesn't exist, or load the existing dataset
if not os.path.exists(dataset_file):
    df = pd.DataFrame(columns=['tag', 'type', 'count'])
else:
    df = pd.read_csv(dataset_file)

# Function to process and extract tags from a given prompt
def extract_tags(prompt, tag_type):
    if len(prompt) == 0:
        return {}
    global df
    tags = set()
    
    # Improve the regular expression pattern to match tags
    
    cleaned_prompt = ''.join(filter(whitelist.__contains__, prompt))
    
    # Extract tags enclosed in parentheses
    extracted_tags = [tag for tag in cleaned_prompt.split(',')]
    
    for t in extracted_tags:
        if len(t) == 0:
            continue
        if t and t[0] == ' ':
            tag = t[1:]
        else:
            tag = t
        tags.add(tag)
    
    # Update the dataset with the extracted tags
    for tag in tags:
        if tag in df['tag'].values:

            # If the tag already exists, update the count
            df.loc[df['tag'] == tag, 'count'] += 1
        else:
            # If it's a new tag, create a new row
            df = df._append({'tag': tag, 'type': tag_type, 'count': 1}, ignore_index=True)
    
    return tags

while True:
    print("")
    # Ask the user for the positive and negative prompts
    positive_prompt = input("Enter the positive prompt: ")
    negative_prompt = input("Enter the negative prompt: ")

    # Extract tags from the positive prompt and update the dataset
    positive_tags = extract_tags(positive_prompt, 'positive')

    # Extract tags from the negative prompt and update the dataset
    negative_tags = extract_tags(negative_prompt, 'negative')

    # Save the updated dataset to the CSV file
    df.to_csv(dataset_file, index=False)

    # Print the extracted tags for reference
    print(f"Positive Tags: {', '.join(positive_tags)}")
    print(f"Negative Tags: {', '.join(negative_tags)}")
