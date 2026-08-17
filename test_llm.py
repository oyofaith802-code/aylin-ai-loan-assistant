from llm import ask_ai


prompt = """
You are Aylin, an AI manager for a pawnshop.

Reply to the customer in Russian.

Customer message:
Здравствуйте, хочу узнать условия займа на автомобиль.
"""


response = ask_ai(prompt)

print("Aylin:")
print(response)