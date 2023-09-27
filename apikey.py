import os

apikey = os.getenv('OPENAI_KEY')
if apikey is None:
    apikey = 'default_value'  # Replace 'default_value' with a string fit for your structure
    print('Default key used')
