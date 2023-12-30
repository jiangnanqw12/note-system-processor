# Regular Expression Utilities

pattern_code_block = r"^    ```(\n[\s\S]*?\n)    ```$"
replacement_code_block = r"    ```python$1    ```"
pattern_star_bullet_list_to_dash_list = r"^(\s*)\*"
replacement_star_bullet_list_to_dash_list = r"\1- "

pattern_old_sub = r'\[\[\d{1,2}:(\d{1,2}:\d{1,2}),\d{1,3} --> \d{1,2}:\d{1,2}:\d{1,2},\d{1,3}\],\[(.*)\]\]'
"""
[[00:00:00,330 --> 00:00:01,750],[哈喽，大家好，我是王刚。]]
"""
replacement_old_sub = r'(\1) \2'
replacement_old_sub2 = r'($1) $2'
