from pynput import keyboard
from pynput.keyboard import Key,Controller
import time 
import httpx
import pyperclip 

from string import Template


controller = Controller()

# Team, I am on leave because of my due to eye conjunctivitis.

# curl -X POST http://localhost:11434/api/generate -H "Content-Type: application/json" -d "{\"model\": \"mistral:7b-instruct-q4_K_S\", \"prompt\": \"Why is the sky blue?\", \"stream\": false}"
#curl http://localhost:11434/api/generate -d "{\"model\": \"mistral:7b-instruct-q4_K_S\",\"prompt\": \"What color is the sky at different times of the day?\",\"stream\": false}"


olama_endpt = "http://localhost:11434/api/generate" 
olama_config = {"model":"mistral:7b-instruct-q4_K_S",
                "keep_alive":"5m",
                "stream":False}

prompt_template = Template(
    '''Correct all the typos and casing and punctuations along with spelling mistakes in this text , but preserve all new line characters you can rearrange the text for proper meaningful sentences:
    
    $text 

    Return only corrected text dont return the preamble.
    
    '''
)

def fixedtext(text):
    prompt = prompt_template.substitute(text=text) 

    responce = httpx.post(olama_endpt,json={"prompt":prompt,**olama_config},
                          headers={"Content-Type":"application/json"},timeout=100) 
    
    if responce.status_code != 200:
        return "Error Caught" 
    else:
        return responce.json()["response"].strip()
                                             



def fix_curr_line():
    controller.press(Key.ctrl) 
    controller.press(Key.shift_l) 

    controller.release(Key.ctrl) 
    controller.release(Key.shift_l) 

    fix_selection()

def fix_selection():
    # 1. copy selection to clipboard 
    with controller.pressed(Key.ctrl):
        controller.tap('c')
    time.sleep(0.1)
    # 2. get the text from clipboard  
    text = pyperclip.paste()
    print(text)
    # 3. fix the text with the help of the LLM 
    fixed_text = fixedtext(text)
    # 4. copy it back to the clipboard
    pyperclip.copy(fixed_text)
    # 5. insert back 
    time.sleep(0.1) 

    with controller.pressed(Key.ctrl):
        controller.tap('v')


    

def on_f9():
    print('F9 pressed')
    fix_curr_line()

def on_f10():
    print('F10 pressed') 
    fix_selection()
    



from pynput.keyboard import Key

print(Key.f9.value,Key.f10.value)


# While running this first check the F9 and F10 keys value by commenting out the below lines


with keyboard.GlobalHotKeys({
        '<120>': on_f9,
        '<121>': on_f10}) as h:
    h.join()

# After you found the values for the F9 and F10 keys replace it inside the < params >
# after running press the f9 and f10 keys respectively to see if they are working fine