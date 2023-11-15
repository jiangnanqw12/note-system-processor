
import pyperclip
import re


def get_prompt_explain_c_cpp(content=None):
    prompt_string1 = '''## Exploring Key C/C++ Concepts: A Guide to Understanding and Resources
Please provide a detailed explanation for the following C/C++ concepts that I'll specify. Can you also recommend some comprehensive books or resources to aid my understanding of these concepts
concepts is :
```
'''
    prompt_string2 = '''```
    '''
    combine_strings_with_clipboard(
        prompt_string1, prompt_string2, content)


def chatbot_prompt_expert(content=None):
    prompt_string1 = '''## chatbot prompt expert

As an AI chatbot prompt expert, could you analyze and provide suggestions to improve the following prompt:
'[
'''
    prompt_string2 = '''
]'
Please provide a final revised version.
'''
    combine_strings_with_clipboard(
        prompt_string1, prompt_string2, content)


def Translate_Chinese_sentence_into_function_name(content=None):
    prompt_string1 = '''
    ## Translate Chinese sentence into function name
Translate the following Chinese sentence into English and create a snake_case function name based on the translated sentence:
[
'''
    prompt_string2 = '''
]. Your function name should reflect the primary task described in the sentence. Please also provide a brief description of what the function will do
'''
    combine_strings_with_clipboard(
        prompt_string1, prompt_string2, content)


def combine_strings_with_clipboard(prompt_string1, prompt_string2, content=None):
    if content is None:
        content = pyperclip.paste()
    final_string = prompt_string1 + content + "\n" + prompt_string2
    pyperclip.copy(final_string)
    # print(final_string)
    return final_string


def Expert_Prompt_Creator():
    final_string = """
I want you to become my Expert Prompt Creator. Your goal is to help me craft the best possible prompt for my needs. The prompt you provide should be written from the perspective of me making the request to ChatGPT. Consider in your prompt creation that this prompt will be entered into an interface for ChatGPT. The process is as follows:
1. You will generate the following sections:

Prompt:
{provide the best possible prompt according to my request}

Critique:
{provide a concise paragraph on how to improve the prompt. Be very critical in your response}

Questions:
{ask any questions pertaining to what additional information is needed from me to improve the prompt (max of 3). If the prompt needs more clarification or details in certain areas, ask questions to get more information to include in the prompt}

2. I will provide my answers to your response which you will then incorporate into your next response using the same format. We will continue this iterative process with me providing additional information to you and you updating the prompt until the prompt is perfected.
Remember, the prompt we are creating should be written from the perspective of me making a request to ChatGPT. Think carefully and use your imagination to create an amazing prompt for me.

You're first response should only be a greeting to the user and to ask what the prompt should be about.
"""
    pyperclip.copy(final_string)
    return final_string


def draw_flowchart():
    """{
  "instruction": "ChatGPT, could you assist me in designing two flowcharts based on the provided code?",
  "codePlaceholder": "[YOUR CODE HERE]",
  "description": "[YOUR CODE DESCRIPTION HERE]",
  "syntax": "Mermaid",
  "flowchartTypes": [
    "high-level overview",
    "detailed, including minor processes"
  ],
  "tone": "formal documentation"
}
"""


def dot2mermaid():
    prompt_string1 = """{ "instruction": "Dear ChatGPT, I need your assistance in converting the following Graphviz code into Mermaid syntax. I'm trying to create a more visually appealing diagram while retaining the structure and relationships depicted in the original Graphviz diagram. Your expertise in this transformation would be highly valued. Here's the Graphviz code:",
 "graphviz_code": "["""
    prompt_string2 = """ ]",
}"""
    content = format_code_2_gpt_input(copy_to_clipboard=False)

    final_string = prompt_string1 + content + prompt_string2
    pyperclip.copy(final_string)


def format_code_2_gpt_input(content=None, copy_to_clipboard=True):
    """
    Formats the input content by replacing multiple newline characters with a single newline character and
    multiple spaces with a single space. If no content is provided, it fetches the content from the clipboard,
    formats it, and then copies the formatted content back to the clipboard if copy_to_clipboard is True.

    :param content: The input content to format. If None, the content will be taken from the clipboard.
    :param copy_to_clipboard: A flag indicating whether to copy the formatted content back to the clipboard.
    :return: The formatted content as a string.
    """
    if content is None:
        try:
            content = pyperclip.paste()
        except pyperclip.PyperclipException:
            print("Unable to access the clipboard.")
            return None

    content = content.replace("\r\n", "\n").replace("\\n", "\n")

    replacements = [
        (r"\n{2,}", "\n"),
        (r"[ ]{2,}", " ")
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    if copy_to_clipboard:
        try:
            pyperclip.copy(repr(content))
        except pyperclip.PyperclipException:
            print("Unable to copy content to the clipboard.")

    return repr(content)


def code_improve():
    prompt_string1 = """{
"language": "Python",
"application_type": "desktop",
"code_snippet": "[ """
    prompt_string2 = """ ]",
"request": "I am developing a desktop application in Python and I need insights on how to improve my code. Here's a snippet of my code. Can you provide feedback on its efficiency, readability, and suggestions for enhancement?"
}"""
    content = format_code_2_gpt_input(copy_to_clipboard=False)

    final_string = prompt_string1 + content + prompt_string2
    pyperclip.copy(final_string)


def video_summarization_expert_one(content=None):

    prompt_string1 = '''## video summarization expert one
Hello ChatGPT,
I have an extensive video subtitle data that needs your expertise. My aim is to break down this data into as many thematic segments as possible, where each segment represents a unique topic or theme discussed in the video.
For each segment, I expect you to craft a detailed summary that includes:
- Title: A descriptive title that encapsulates the main point of the segment.
- Start Timestamp: The starting time of the segment within the video.
- Summary: A brief and short summary text showing the main points or topics discussed in that segment.
Here is the format I expect for each segment:
Title:
Start Timestamp:
Summary:
Kindly start analyzing the following subtitle data:
[
'''
    prompt_string2 = '''
]
I appreciate your assistance. Thank you!
'''
    content = format_code_2_gpt_input(copy_to_clipboard=False)

    final_string = prompt_string1 + content + prompt_string2
    pyperclip.copy(final_string)
