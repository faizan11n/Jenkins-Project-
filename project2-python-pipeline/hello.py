from datetime import datetime

message = f"Hello from Jenkins pipeline! Run time: {datetime.now()}"
print(message)

with open("result.txt", "w") as f:
    f.write(message + "\n")

