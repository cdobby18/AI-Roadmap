from transformers import pipeline

chatbot = pipeline("text-generation", model="gpt2")

prompt = "User: Hello\nBot:"

response = chatbot(prompt, max_length=50)

print(response)