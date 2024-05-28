import os.path

BIN = os.path.exists("./notifications/wiki_query.txt")

if os.path.exists("./notifications/wiki_query.txt"):
    f1 = open("./notifications/wiki_query.txt", 'r')
    prompt = f1.read()
    f1.close()
print(prompt)
print(type(prompt))