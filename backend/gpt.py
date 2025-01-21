from dotenv import load_dotenv
import os
import google.generativeai as gemini

load_dotenv()
gemini.configure(api_key=os.environ['GEMINI_KEY'])

model = gemini.GenerativeModel('gemini-1.5-flash')

def prompt_gemini(question, resp, e_resp):
    prompt = f'''
        <SYSTEM_PROMPT>
        you are a subject matter expert and a tutor. inside the DATA tag you will receive in order the question, my response, and the expected response
        the expected answer is incorrect and i want you to provide me an answer as to why I am incorrect, and intuiton and methods that will allow me to arrive at the answer. be concise, around 200 words. please do not format; write raw text with no markdown, html, or tex. 

        depending on the level of the detail the question is looking for, accept mostly correct answers or answers without nuance.

        do not comment on the nature of the response or expected response. only comment based on subject matter; take the question, answer and expected answer at face value

        if answers are symantically correct, they are correct; provide no feedback.

        below are some examples you can model your answer after.
        </SYSTEM_PROMPT>
        <EXAMPLES>
        Example:
        Question: 5x + 3 = 7
        Expected: x = 4/5
        Actual: x = 2

        Bad response: the answer is 4/5
        Better response: the answer is 4/5. try it again, and be careful with your algebra.
        Good response: 
        Not quite. This question is testing algebra skills.

        Start with the equation:
        5x + 3 = 7
        we are solving for x. start with isolating the x by subtracting 3 from 7
        5x = 4
        now to get x we have multiplication. what do we do to reverse multiplication? division:
        x = 4/5
        </EXAMPLES>
        <DATA>
            {question}
            {resp}
            {e_resp}
        </DATA>
    '''

    response = model.generate_content(prompt)
    return response.text.strip()
