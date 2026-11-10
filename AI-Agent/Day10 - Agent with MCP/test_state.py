from state import *

state=create_state("Generate a password and tell me the current time")
print("Initial state")
print(state)

add_action(
    state,
    "generate_password"
)

print("action added")

record_observation(
    state,
    "generate_password",
    "Password : Zw!@DSD!@Es"
)

next_step(state)

print("\nState after one Iteration")

print(state)

print(record_observation)

