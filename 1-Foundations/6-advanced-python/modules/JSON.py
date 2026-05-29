import json
data = {"name":"Carl","age":25}
with open("data.json","w") as f:
    json.dump(data, f)

with open("data.json","r") as f:
    data_loaded = json.load(f)
print(data_loaded)