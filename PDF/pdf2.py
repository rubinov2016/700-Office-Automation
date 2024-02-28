import openai
import os
from time import time, sleep
import textwrap
import re

# Function to read API key from a file
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Setting up OpenAI API key
openai.api_key = open_file('1.key')

# Function to save content to a file
def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

# Function to get GPT-3 completion
def gpt3_completion(prompt, engine='text-davinci-003', temp=0.6, top_p=1.0, tokens=2000, freq_pen=0.25, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response.choices[0].text.strip()
            text = re.sub('\s+', ' ', text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return f"GPT3 error: {oops}"
            print('Error communicating with OpenAI:', oops)
            sleep(1)

if __name__ == '__main__':
    # Reading input text
    alltext = open_file('input.txt')
    # Splitting input text into chunks
    chunks = textwrap.wrap(alltext, 2000)
    result = list()
    count = 0
    # Processing each chunk
    for chunk in chunks:
        count += 1
        # Reading prompt
        prompt = open_file('prompt.txt').replace('<<SUMMARY>>', chunk)
        prompt = prompt.encode(encoding='ASCII', errors='ignore').decode()
        # Generating summary using GPT-3
        summary = gpt3_completion(prompt, engine='gpt-3.5-turbo')
        print('\n\n\n', count, 'of', len(chunks), ' - ', summary)
        result.append(summary)
    # Saving output
    output_filename = f'output_{time()}.txt'
    save_file('\n\n'.join(result), output_filename)
    print(f"Output saved to {output_filename}")
