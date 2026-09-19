import ollama

thething = input("Enter your thing here: ")
stream = ollama.chat(
    model='qwen2.5:7b',
    messages=[{'role': 'user', 'content': thething}],
)

print(stream.message['content'])
