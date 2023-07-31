from pathlib import Path
import subprocess

print(
"""(1) Paste your URLs here, separated by newlines, and then input "done".
Do not paste the full URLs, just the parts relative to the current folder.
Do not start with a slash.


Example: 

images/model-bg.933dddb8..png
images/share-bg.ceeffebf..png
images/confirm-bg.d6b68bce..png
images/kv-bg.17cbf8e7..png
done
"""
)

files = []

while True:
    user_input = input()
    if user_input.lower() == "done":
        break
    if user_input != "":
        files.append(user_input)


print(
"""(2) Paste your URL to be prefixed at the start of every URL. End with a slash. 

Example:

https://act.hoyoverse.com/bh3/event/e20230724music/
"""
)

url_prefix = input()

procs = []

for file in files:
    file_dir = str(Path(file).parent)
    download_url = url_prefix+file
    Path(file_dir).mkdir(exist_ok=True, parents=True)
    command = ["aria2c", f"--dir={file_dir}", "--continue", download_url]    
    proc = subprocess.Popen(command)
    procs.append(proc)

print("waiting for procs to finish...")

return_codes = [x.wait() for x in procs]
print("return codes: ", return_codes)

print("done!")