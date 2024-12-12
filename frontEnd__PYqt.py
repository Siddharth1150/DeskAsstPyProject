import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt


class ChatBotApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NOVA")
        self.setGeometry(200, 100, 800, 600)

        self.initUI()

    def initUI(self):
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Top Section: AI Name and Logo
        top_section = QHBoxLayout()
        ai_name_logo = QLabel("🤖 NOVA")
        ai_name_logo.setStyleSheet("font: bold 20pt; color: blue;")
        ai_name_logo.setFixedSize(150, 50)
        ai_name_logo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        top_section.addWidget(ai_name_logo)

        # Spacer for alignment
        top_section.addStretch(1)

        # Internet Signal Status
        internet_status = QLabel("Internet: Connected")
        internet_status.setStyleSheet("font: 10pt; color: green;")
        top_section.addWidget(internet_status)

        # Add to main layout
        main_layout.addLayout(top_section)

        # Chat Area
        chat_area = QVBoxLayout()

        # Chat history
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("background-color: lightgray; font: 12pt; padding: 5px;")
        chat_area.addWidget(self.chat_history)

        # Add chat area to main layout
        main_layout.addLayout(chat_area)

        # Bottom Section: Mic and Input Field
        bottom_section = QHBoxLayout()

        mic_button = QPushButton("🎤 Mic")
        mic_button.setStyleSheet("background-color: lightblue; font: 12pt; padding: 5px;")
        mic_button.setFixedSize(80, 40)
        bottom_section.addWidget(mic_button)

        # Message input field with dynamic resizing
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.setStyleSheet("font: 12pt; padding: 5px;")
        self.message_input.setMinimumHeight(40)
        self.message_input.setMaximumHeight(40)

        bottom_section.addWidget(self.message_input)

        send_button = QPushButton("Send")
        send_button.setStyleSheet("background-color: lightgreen; font: 12pt; padding: 5px;")
        send_button.setFixedSize(100, 40)
        send_button.clicked.connect(self.send_message)
        bottom_section.addWidget(send_button)

        # Add bottom section to main layout
        main_layout.addLayout(bottom_section)

        # Set main layout to the window
        self.setLayout(main_layout)

    def resizeEvent(self, event):
        """Adjust the message input box width dynamically to 50% of the window's width."""
        window_width = self.width()
        new_width = int(window_width * 0.5)  # Convert to integer
        self.message_input.setFixedWidth(new_width)
        super().resizeEvent(event)


    def send_message(self):
        user_text = self.message_input.text()
        if user_text:
            # Display user text in chat history
            self.chat_history.append(f"You: {user_text}")

            # Placeholder AI response
            ai_response = "This is a placeholder response."
            self.chat_history.append(f"AI: {ai_response}")

            # Clear the input field
            self.message_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chatbot = ChatBotApp()
    chatbot.show()
    sys.exit(app.exec_())



# import sys
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QScrollArea
# )
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QIcon

# class ChatBotApp(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("NOVA")
#         self.setGeometry(200, 100, 800, 600)

#         self.initUI()

#     def initUI(self):
#         # Main Layout
#         main_layout = QVBoxLayout()
#         main_layout.setContentsMargins(10, 10, 10, 10)

#         # Chat Area
#         chat_area = QTextEdit()
#         chat_area.setReadOnly(True)
#         chat_area.setStyleSheet("background-color: lightgray; font: 12pt; border: none;")
#         main_layout.addWidget(chat_area)

#         # Message Input Section
#         message_layout = QHBoxLayout()
#         message_layout.setContentsMargins(0, 0, 0, 0)

#         # Icon on the left
#         left_icon = QPushButton("+")
#         left_icon.setFixedSize(40, 40)
#         left_icon.setStyleSheet(
#             """
#             QPushButton {
#                 border-radius: 20px;
#                 background-color: #282A36;
#                 color: white;
#                 font: bold 16pt;
#             }
#             QPushButton:hover {
#                 background-color: #44475A;
#             }
#             """
#         )
#         message_layout.addWidget(left_icon)

#         # Message input box
#         self.message_input = QLineEdit()
#         self.message_input.setPlaceholderText("Message Copilot")
#         self.message_input.setStyleSheet(
#             """
#             QLineEdit {
#                 background-color: #1E1F29;
#                 color: white;
#                 font: 14pt;
#                 border: none;
#                 border-radius: 20px;
#                 padding: 10px;
#                 margin-left: 5px;
#                 margin-right: 5px;
#             }
#             """
#         )
#         self.message_input.setMinimumHeight(40)
#         message_layout.addWidget(self.message_input)

#         # Mic button on the right
#         mic_button = QPushButton()
#         mic_button.setIcon(QIcon("mic_icon.png"))  # Replace with the actual path to your mic icon
#         mic_button.setFixedSize(40, 40)
#         mic_button.setStyleSheet(
#             """
#             QPushButton {
#                 border-radius: 20px;
#                 background-color: #282A36;
#             }
#             QPushButton:hover {
#                 background-color: #44475A;
#             }
#             """
#         )
#         message_layout.addWidget(mic_button)

#         # Add the message layout to the main layout
#         main_layout.addLayout(message_layout)

#         # Set the main layout to the window
#         self.setLayout(main_layout)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     chatbot = ChatBotApp()
#     chatbot.show()
#     sys.exit(app.exec_())
