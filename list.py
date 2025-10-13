import os
directory_path = "."
# Use os.walk to list all files, including those in subdirectories
for dirpath, dirnames, filenames in os.walk(directory_path):
    dirnames[:] = [d for d in dirnames if "git" not in d]
    for filename in [f for f in filenames if not f.startswith("README.md") and f.endswith('.md')]:
        print(os.path.join(dirpath, filename))