from openai import OpenAI
# Documentation: https://platform.openai.com/docs/quickstart?context=python

client = OpenAI()
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )

# See which models you have access to in the playground model selection tab:
# https://platform.openai.com/playground


completion = client.chat.completions.create(
  model="gpt-4",  # "gpt-3.5-turbo"
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)