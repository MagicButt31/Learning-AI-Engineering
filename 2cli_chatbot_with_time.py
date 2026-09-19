import ollama
import time

thething = input("Enter your thing here: ")
current_time = time.time() #start of timer
stream = ollama.chat(
    model='qwen2.5:7b',
    messages=[{'role': 'user', 'content': thething}],
)

print(stream.['message']['content'], end='', flush=True)
print("\n")

#time finished, now time taken for the response to be generated is calculated
current_time = time.time() - current_time
print(f"Time taken: ~{round(current_time, 2)} seconds")
