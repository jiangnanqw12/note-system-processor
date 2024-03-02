import pyperclip
import re


def create_node_for_mermaid(num=30):
    content = ""
    for i in range(num):
        content += f"Node_{i+1}[\"\"]\n"

    pyperclip.copy(content)


def convert_array_to_mermaid_nodes():
    # Define the array of error descriptions
    error_desc = ["无错误", "换能器未连接", "换能器不兼容", "换能器无剩余使用次数",
                  "换能器未拧紧", "检测到刀头错误", "减轻刀头压力", "换能器损坏",
                  "风扇错误", "手控或脚踏开关可能被卡住", "过压错误", "过流错误",
                  "电源错误", "场效应管错误", "主机过热", "主机错误"]

    # Convert to Mermaid nodes
    mermaid_nodes = ["graph TD"]
    for i, desc in enumerate(error_desc, start=1):
        mermaid_nodes.append(f'    Node_{i}["{desc}"]')

    # Join to form the complete Mermaid output
    mermaid_output = '\n'.join(mermaid_nodes)
    pyperclip.copy(mermaid_output)


def test1():
    nodes = [
        "Node_0[\"error_desc\"]",
        "Node_1[\"无错误\"]",
        "Node_2[\"换能器未连接\"]",
        "Node_3[\"换能器不兼容\"]",
        "Node_4[\"换能器无剩余使用次数\"]",
        "Node_5[\"换能器未拧紧\"]",
        "Node_6[\"检测到刀头错误\"]",
        "Node_7[\"减轻刀头压力\"]",
        "Node_8[\"换能器损坏\"]",
        "Node_9[\"风扇错误\"]",
        "Node_10[\"手控或脚踏开关可能被卡住\"]",
        "Node_11[\"过压错误\"]",
        "Node_12[\"过流错误\"]",
        "Node_13[\"电源错误\"]",
        "Node_14[\"场效应管错误\"]",
        "Node_15[\"主机过热\"]",
        "Node_16[\"主机错误\"]"
    ]

    # Generate links
    links = [f'Node_0-->{i}-->Node_{i + 1}' for i in range(len(nodes) - 1)]

    # Combine nodes and links for Mermaid output
    mermaid_output = '\n'.join(["graph TD"] + nodes + links)

    pyperclip.copy(mermaid_output)


def mermaid_format(content=None):

    if content is None:
        content = pyperclip.paste()
    # content = repr(content)
    print(repr(content))
    # content = content.replace(" \w{1,3}", "\n")
    num_str = r"22"
    reg_repalce_list = []
    reg_repalce_list.append(
        [r" (\w{1,3})( |\n|\(|\{|\[)", r" \1_"+num_str+r"\2"])
    # reg_repalce_list.append([r" \w{1,3}\n", r" \1\n"+num_str])
    for reg_replace in reg_repalce_list:
        content = re.sub(reg_replace[0], reg_replace[1], content)
    print(repr(content))
    # Copying the formatted content back to the clipboard
    pyperclip.copy(content)
