import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

system_messages = [{"role" : "system", "content" : "you're an assistant"}, {"role" : "user", "content" : "give me a list of bullet points"}]
def main():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=system_messages,
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    #print(response)


main()