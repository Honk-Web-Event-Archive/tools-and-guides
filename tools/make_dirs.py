from pathlib import Path

print("Paste url link to create directories recursively:")
link = input()
link = str(Path(link).parent).split("\\")[2:]
link = '/'.join(link)
print("Directory is: ",link)
Path(link).mkdir(parents=True)
print("Directories created!")