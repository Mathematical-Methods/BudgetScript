import ollama

#Return the receipt timestamp in MM-DD-YYYY:
text = ''' You are in charge of reading the following text from a receipt and returning only one of the following categories: "income", "return", "payroll", "debt", "debts", "housing", "insurance", "investment", "savings", "saving", "medical", "misc", "personal", "transportation", "gas", "utilities", "food", "donation"

'''

response = ollama.chat(model='qwen2:0.5b', messages=[
  {
    'role': 'user',
    'content': text,
  },
])
print(response['message']['content'])