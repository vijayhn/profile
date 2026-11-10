from memory_extractor import extract_memory


memory = extract_memory(
    "Hi my name is Vijay & I love Cto study snakes",
    "Hey Vijay, its great to know you love to study snakes, do you want any help"
)

print("Extracted Memory:")

print(memory)
