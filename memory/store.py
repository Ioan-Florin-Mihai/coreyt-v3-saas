import json
import os

MEMORY_FILE = "memory\data.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)


def add_message(user_id, role, content):
    memory = load_memory()

    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append({"role": role, "content": content})

    save_memory(memory)


def get_messages(user_id):
    memory = load_memory()
    return memory.get(user_id, [])
