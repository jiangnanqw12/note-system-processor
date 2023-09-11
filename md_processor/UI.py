import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QPushButton, QTextEdit
import prompts
import pyperclip

# Your functions here (e.g., get_prompt_explain_c_cpp, video_summarization_expert_one, Translate_Chinese_sentence_into_function_name)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        tab_widget = QTabWidget()

        prompts_tab = QWidget()
        prompts_layout = QVBoxLayout()

        self.prompts_text_edit = QTextEdit()
        prompts_layout.addWidget(self.prompts_text_edit)

        btn1 = QPushButton('video_summarization_expert_one')
        btn1.clicked.connect(lambda: prompts.video_summarization_expert_one(
            self.prompts_text_edit.toPlainText()))
        prompts_layout.addWidget(btn1)

        btn2 = QPushButton('Get Prompt Explain C/C++')
        btn2.clicked.connect(lambda: prompts.get_prompt_explain_c_cpp(
            self.prompts_text_edit.toPlainText()))
        prompts_layout.addWidget(btn2)

        btn3 = QPushButton('chatbot_prompt_expert')
        btn3.clicked.connect(lambda: prompts.chatbot_prompt_expert(
            self.prompts_text_edit.toPlainText()))
        prompts_layout.addWidget(btn3)

        btn4 = QPushButton('Translate Chinese Sentence into Function Name')
        btn4.clicked.connect(lambda: prompts.Translate_Chinese_sentence_into_function_name(
            self.prompts_text_edit.toPlainText()))
        prompts_layout.addWidget(btn4)

        btn5 = QPushButton('Expert_Prompt_Creator')
        btn5.clicked.connect(lambda: prompts.Expert_Prompt_Creator(
            self.prompts_text_edit.toPlainText()))
        prompts_layout.addWidget(btn5)

        prompts_tab.setLayout(prompts_layout)
        tab_widget.addTab(prompts_tab, "Prompts")

        layout.addWidget(tab_widget)

        self.setLayout(layout)
        self.setWindowTitle('Expert Prompt Creator')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
