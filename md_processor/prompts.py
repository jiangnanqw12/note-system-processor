
import pyperclip


def get_prompt_explain_c_cpp():
    prompt_string1 = '''## Exploring Key C/C++ Concepts: A Guide to Understanding and Resources
Please provide a detailed explanation for the following C/C++ concepts that I'll specify. Can you also recommend some comprehensive books or resources to aid my understanding of these concepts
concepts is :
```
'''
    prompt_string2 = '''```
    '''
    combine_strings_with_clipboard(prompt_string1, prompt_string2)


def video_summarization_expert_one():
    """
## video summarization expert one
Hello ChatGPT,
I have an extensive video subtitle data in SRT format that needs your expertise. My aim is to break down this data into as many thematic segments as possible, where each segment represents a unique topic or theme discussed in the video.
For each segment, I expect you to craft a detailed summary that includes:
- Title: A descriptive title that encapsulates the main point of the segment.
- Start Timestamp: The starting time of the segment within the video.
- Summary: A concise summary text detailing the main points or topics discussed in that segment.
Here is the format I expect for each segment:
Title:
Start Timestamp:
Summary:
Kindly start analyzing the following SRT data:
[

]
I appreciate your assistance. Thank you!
"""
    prompt_string1 = '''## video summarization expert one
Hello ChatGPT,
I have an extensive video subtitle data in SRT format that needs your expertise. My aim is to break down this data into as many thematic segments as possible, where each segment represents a unique topic or theme discussed in the video.
For each segment, I expect you to craft a detailed summary that includes:
- Title: A descriptive title that encapsulates the main point of the segment.
- Start Timestamp: The starting time of the segment within the video.
- Summary: A concise summary text detailing the main points or topics discussed in that segment.
Here is the format I expect for each segment:
Title:
Start Timestamp:
Summary:
Kindly start analyzing the following SRT data:
[
'''
    prompt_string2 = '''
]
I appreciate your assistance. Thank you!
'''
    combine_strings_with_clipboard(prompt_string1, prompt_string2)


def chatbot_prompt_expert():
    prompt_string1 = '''## chatbot prompt expert

As an AI chatbot prompt expert, could you analyze and provide suggestions to improve the following prompt:
'[
'''
    prompt_string2 = '''
]'
Please provide a final revised version.
'''
    combine_strings_with_clipboard(prompt_string1, prompt_string2)


def Translate_Chinese_sentence_into_function_name():
    prompt_string1 = '''
    ## Translate Chinese sentence into function name
Translate the following Chinese sentence into English and create a snake_case function name based on the translated sentence:
[
'''
    prompt_string2 = '''
]. Your function name should reflect the primary task described in the sentence. Please also provide a brief description of what the function will do
'''
    combine_strings_with_clipboard(prompt_string1, prompt_string2)


def combine_strings_with_clipboard(prompt_string1, prompt_string2):
    string3 = pyperclip.paste()
    final_string = prompt_string1 + string3 + "\n" + prompt_string2
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
