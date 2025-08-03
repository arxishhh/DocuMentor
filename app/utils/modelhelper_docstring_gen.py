import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from app.utils.code_comment_extractor import finding_func

def generating_docstring(file):
    functions = finding_func(file)
    df = pd.DataFrame()
    df['Code'] = functions
    load_dotenv()
    prompt = '''
    Generate a concise and professional Python docstring for the given function.
Do not include the function definition or any code.
Ignore any comments within the code.
Do not add any preamble, explanation, or formatting outside the docstring body.
Take the help from examples to formulate your result
    ### Code:
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

### Docstring:
"""Check if a number is prime.

Args:
    n (int): The number to check.

Returns:
    bool: True if the number is prime, False otherwise.
"""
### Code:
def get_user_initials(name):
    return ''.join([word[0].upper() for word in name.split()])

### Docstring:
"""Return the initials of a user's full name.

Args:
    name (str): Full name of the user.

Returns:
    str: Initials in uppercase (e.g., "J.D." for "John Doe").
"""
Code 
=======
{code}
    '''
    response = []
    llm = ChatGroq(model = 'llama-3.3-70b-versatile',temperature = 0.9)
    pt = PromptTemplate.from_template(prompt)
    chain = pt | llm
    for code in functions:
        res = chain.invoke({'code': code})
        response.append(res.content)
        print(res.content)
    df['DocString'] = response
    return df

if __name__ == '__main__':
    print(generating_docstring('sample.py'))


