import os 
import json

# Remove file
for i in ["joined_group.json", "score.json","total_score.json"]:
    os.remove(f"cache/{i}")

# Make null joined_group json file 
with open("cache/joined_group.json","w") as data:
    data.write(json.dumps({"groups":[]}, indent=4))

# Make null joined_group json file 
with open("cache/total_score.json","w") as data:
    data.write(json.dumps({"score":[]}, indent=4))


# Make null score json file
with open("cache/score.json","w") as data:
    data.write(json.dumps({"score":[]}, indent=4))

print("Done.")