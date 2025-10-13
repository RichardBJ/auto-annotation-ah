"""From here:
Transcriptomic cell-type diversity across the adult human brain
Siletti et al. 2022
https://github.com/linnarsson-lab/auto-annotation-ah
"""


import pandas as pd
import os, re

# Define the directory path
directory_path = "."
patterns = ['name:', 'abbreviation:', 'definition:']
names = []
abbrs = []
posdefs = []
negdefs = []
files = []
paths = []

def process_defs(terms):
    # Split the string into a list of terms
    terms_list = terms.split(" ")
    positive = [" "]
    negative = [" "]
    for term in terms_list:
        # If the term starts with '+', add it to the positive list
        if term.startswith("+"):
            positive.append(term[1:])
        # If the term starts with '-', add it to the negative list
        elif term.startswith("-"):
            negative.append(term[1:])
    return positive, negative

# Use os.walk to list all files, including those in subdirectories
for dirpath, dirnames, filenames in os.walk(directory_path):
    dirnames[:] = [d for d in dirnames if "git" not in d]
    for filename in [f for f in filenames if not f.startswith("README.md") and f.endswith('.md')]:
        with open(os.path.join(dirpath, filename), 'r') as file:
            print(os.path.join(dirpath, filename))
            content = file.read()
            for pattern in patterns:
                match = re.search(f'{pattern} (.*)', content)
                if match:
                    term = f"{pattern} {match.group(1)}" 
                    if pattern == "name:": names.append(match.group(1))
                    elif pattern == "abbreviation:": abbrs.append(match.group(1))
                    elif pattern == "definition:": 
                        pos, neg = process_defs(match.group(1))
                        posdefs.append(",".join(pos))
                        negdefs.append(",".join(neg))
            paths.append(dirpath)
            files.append(filename)

df = pd.DataFrame({
    "Path":paths, 
    "File":files, 
    "Name":names,
    "Abbreviation":abbrs,
    "Positives":posdefs,
    "Negatives":negdefs})                        
print(df.head())
df.to_csv("terms.txt", sep="\t")
