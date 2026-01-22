import os
from groq import Groq
c = Groq(api_key=os.getenv("GROQ_API_KEY"))
print("Groq client loaded. chat object type:", type(c.chat))
print("Public attributes/methods on c.chat:")
print([a for a in dir(c.chat) if not a.startswith("_")])
