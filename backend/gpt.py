from dotenv import load_dotenv
import os
import google.generativeai as gemini

load_dotenv()
gemini.configure(api_key=os.environ['GEMINI_KEY'])

model = gemini.GenerativeModel('gemini-1.5-flash')

def prompt_gemini(question, resp, e_resp):
    prompt = f'''
        <SYSTEM_PROMPT>
        you are a subject matter expert and a tutor. you will receive a question, answer, and expected answer.
        the expected answer is incorrect and i want you to provide an indepth response to the user is incorrect, and the correct solution. provide some intuition and reasoning depending on the complexity of the problem. be concise, around 200 words. format in html inside a div block but don't add markdown escape ticks.
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

        The question is {question}
        The response is {resp}
        The correct answer is {e_resp}
    '''

    response = model.generate_content(prompt)
    return response.text.strip()
