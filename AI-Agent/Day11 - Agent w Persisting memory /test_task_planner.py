from task_planner import decompose_task


user_request = (
    "Get the current time and tell me my name"
)


tasks = decompose_task(user_request)


print("\nTask Plan")
print("---------")

for task in tasks:
    print("-", task)
