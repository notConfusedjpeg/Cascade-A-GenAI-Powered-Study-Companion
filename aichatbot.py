import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
import google.generativeai as genai

# Configure the API key for the generative AI model
genai.configure(api_key=("AIzaSyBGNy7MMFxMmwgmLtU9wVp-TdB9jhyCNwY"))

# Initialize the generative model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Function to get a response and a title for the query
def get_gemini_response(question):
    # Generate a response from the chat model
    response = chat.send_message(question, stream=True)
    
    # Simple title generation based on the question
    title = question.capitalize() 
    
    return title, response

# Main application class
class GeminiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.title = QLabel('Gemini Application')
        self.input = QLineEdit(self)
        self.askButton = QPushButton('Ask the question', self)
        self.responseArea = QTextEdit(self)

        layout.addWidget(self.title)
        layout.addWidget(self.input)
        layout.addWidget(self.askButton)
        layout.addWidget(self.responseArea)

        self.askButton.clicked.connect(self.on_click)

        self.setWindowTitle('Q&A Demo')
        self.show()

    def on_click(self):
        question = self.input.text()
        title, response = get_gemini_response(question)
        self.responseArea.clear()
        self.responseArea.append(f"<h2>{title}</h2>")
        for chunk in response:
            self.responseArea.append(chunk.text)
        self.responseArea.append('_'*80)

        # Start of the chat history section with a title
        self.responseArea.append("<h2>Chat History</h2>")
        
        # Iterate over the chat history and format it with HTML
        for entry in chat.history:
            if hasattr(entry, 'question_text') and hasattr(entry, 'response_text'):
                # User question with a darker background
                self.responseArea.append(f"<div style='background-color:#D3D3D3;'>Q: {entry.question_text}</div>")
                # Model response with a lighter background
                self.responseArea.append(f"<div style='background-color:#F5F5F5;'>A: {entry.response_text}</div>")
        
        # Separator after the chat history
        self.responseArea.append('_'*80)

# Entry point of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GeminiApp()
    sys.exit(app.exec_())
