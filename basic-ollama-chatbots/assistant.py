import ollama
import time
import keyboard
import os
import json

ai_model = 'qwen2.5:7b'
def main():
    clearterminal()
    with open("ai_history.json", "r", encoding="utf-8") as file:
        totalmessagelist = file.read()
    if totalmessagelist == "":
        totalmessagelist = []
    else:
        totalmessagelist = [item for item in json.loads(totalmessagelist)]
    while True:
        ai_inp = input("Ask the AI anything (enter '/help' for commands): ")
        try:
            response_quitted = False
            response_written = []
            ai_message = {'role': 'user', 'content': ai_inp}
            a = ""
            if ai_inp.find("/") == 0:
                if ai_inp == "/quit":
                    break
                elif ai_inp == "/help":
                    print("""Commands:
                    /quit: quits the program
                    /clearhistory: clears response history
                    /read: reads chat history""")
                elif ai_inp == "/clearhistory":
                    clearterminal()
                    with open("ai_response.txt", "w", encoding="utf-8") as file:
                        file.write("")
                    with open("ai_history.json", "w", encoding="utf-8") as file:
                        file.write("")
                        totalmessagelist = []
                    print("history cleared")
                elif ai_inp == "/read":
                    with open("ai_response.txt", "r", encoding="utf-8") as file:
                        read = file.read()
                    print(read)
                else:
                    print("Command doesn't exist.")
            else:
                with open("ai_response.txt", "a", encoding="utf-8") as file:
                    file.write("User: " + ai_inp + "\n")
                totalmessagelist.append(ai_message)
                print("Generating response...")
                current_time = time.time() #start of timer
                stream = ollama.chat(
                    model=ai_model,
                    messages=totalmessagelist,
                    options={'num_ctx': 8192,},
                    stream=True,
                )
                #what stream=True does is lets you see the response being generated in real time
                #instead of waiting for the entire response to be generated before you see it
                for chunk in stream: #This loop goes through each chunk of the response as it's generated
                    print(chunk['message']['content'], end='', flush=True)
                    response_written.append(chunk['message']['content'])
                    if keyboard.is_pressed('esc'):
                        print("\nResponse has been quitted.")
                        response_quitted = True
                        response_written.clear()
                        break
                print("\n")
    
                if response_quitted == False:
                    x = "".join(response_written)
                    y = ''.join(response_written)
                    a = {'role': 'assistant', 'content': y}
                    totalmessagelist.append(a)
                    with open("ai_response.txt", "a", encoding="utf-8") as file:
                        file.write("Assistant: " + x + "\n")
                    x = ""
                    with open("ai_history.json", "w", encoding="utf-8") as file:
                        file.write(json.dumps(totalmessagelist, indent=4))
                #time finished, now we calculate the time taken for the response to be generated
                current_time = time.time() - current_time
                print(f"Time taken: ~{round(current_time, 2)} seconds")
        except KeyboardInterrupt:
            clearterminal()
            print("\n ctrl+c will not work. Please use /quit to quit.")

def clearterminal():
    os.system('cls' if os.name == 'nt' else 'clear')

main()