from openai import OpenAI

# initialize client with your API key
client = OpenAI(api_key="AIzaSyB1wRE0oD0z0QNOGzy6Wu7dYO8ohvVi_tQ")

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "what is coding."}
    ]
)

print(completion.choices[0].message["content"])
