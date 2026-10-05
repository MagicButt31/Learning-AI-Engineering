import ollama
import time

thething = input("Enter your thing here: ")
current_time = time.time()
stream = ollama.chat(
    model='qwen2.5:7b',
    messages=[{'role': 'user', 'content': thething}],
    stream=True,
)
#what stream=True does is lets you see the response being generated in real time
#instead of waiting for the entire response to be generated before you see it

for chunk in stream: #This loop goes through each chunk of the response as it's generated
    print(chunk['message']['content'], end='', flush=True)
print("\n")

current_time = time.time() - current_time
print(f"Time taken: ~{round(current_time, 2)} seconds")
