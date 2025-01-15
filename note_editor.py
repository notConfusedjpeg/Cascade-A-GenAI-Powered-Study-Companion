import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QInputDialog, QFontDialog, QMessageBox, QTabWidget, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QTextCursor, QTextDocument
from PyQt5.QtCore import Qt
import os
import resourcesCascade

class ReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Replace Text")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout(self)

        self.find_label = QLabel("Find:", self)
        self.find_input = QLineEdit(self)

        self.replace_label = QLabel("Replace with:", self)
        self.replace_input = QLineEdit(self)

        self.replace_button = QPushButton("Replace", self)
        self.replace_button.clicked.connect(self.accept)

        layout.addWidget(self.find_label)
        layout.addWidget(self.find_input)
        layout.addWidget(self.replace_label)
        layout.addWidget(self.replace_input)
        layout.addWidget(self.replace_button)

    def get_inputs(self):
        return self.find_input.text(), self.replace_input.text()

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()

        self.predefined_folder = os.path.expanduser(r"data\notepad_data")
        if not os.path.exists(self.predefined_folder):
            os.makedirs(self.predefined_folder)

        self.tabs_widget = QTabWidget()
        self.tabs_widget.setTabsClosable(True)
        self.tabs_widget.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs_widget)

        self.tabs = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Notepad')
        icon = QtGui.QIcon(":/images/images for cascade/notes_icon.png")
        self.setWindowIcon(icon)
        self.setStyleSheet("background-color: #a791cb;")
        self.setGeometry(100, 100, 800, 600)

        # Create actions
        new_tab_action = self.create_action('New Tab', 'Ctrl+T', self.new_tab)
        new_window_action = self.create_action('New Window', 'Ctrl+N', self.new_window)
        close_tab_action = self.create_action('Close Tab', 'Ctrl+W', lambda: self.close_tab(self.tabs_widget.currentIndex()))
        close_window_action = self.create_action('Close Window', 'Ctrl+Shift+W', self.close_window)
        open_action = self.create_action('Open', 'Ctrl+O', self.open_file)
        exit_action = self.create_action('Exit', 'Ctrl+Q', self.close)
        rename_action = self.create_action('Rename', None, self.rename_file)
        save_action = self.create_action('Save', 'Ctrl+S', self.save_file)
        save_as_action = self.create_action('Save As', 'Ctrl+Shift+S', self.save_as_file)

        # Create menubar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        file_menu.addActions([new_tab_action, new_window_action, open_action, close_tab_action, close_window_action])
        file_menu.addSeparator()
        file_menu.addAction(rename_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addAction(exit_action)

        find_action = self.create_action('Find', 'Ctrl+F', self.find_text)
        find_next_action = self.create_action('Find Next', 'F3', self.find_next)
        find_prev_action = self.create_action('Find Previous', 'Shift+F3', self.find_prev)
        replace_action = self.create_action('Replace', 'Ctrl+H', self.replace_text)

        goto_action = self.create_action('Go To', 'Ctrl+G', self.go_to)

        font_action = self.create_action('Font', None, self.change_font)

        zoom_in_action = self.create_action('Zoom In', 'Ctrl++', self.zoom_in)
        zoom_out_action = self.create_action('Zoom Out', 'Ctrl+-', self.zoom_out)

        word_wrap_action = self.create_action('Word Wrap', None, self.toggle_word_wrap)
        status_bar_action = self.create_action('Status Bar', None, self.toggle_status_bar)

        # Add actions to menubar
        edit_menu = menubar.addMenu('Edit')
        edit_menu.addActions([find_action, find_next_action, find_prev_action, replace_action])
        edit_menu.addAction(goto_action)

        format_menu = menubar.addMenu('Format')
        format_menu.addAction(font_action)

        view_menu = menubar.addMenu('View')
        view_menu.addActions([zoom_in_action, zoom_out_action])
        view_menu.addAction(word_wrap_action)
        view_menu.addAction(status_bar_action)

        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready')

        self.new_tab()

    def create_action(self, text, shortcut, function):
        action = QAction(text, self)
        if shortcut:
            action.setShortcut(shortcut)
        action.triggered.connect(function)
        return action

    def save_file(self):
        current_tab = self.tabs_widget.currentWidget()
        if current_tab:
            note_name = self.tabs_widget.tabText(self.tabs_widget.currentIndex())
            if note_name == "Untitled":
                note_name, ok = QInputDialog.getText(self, "Save Note", "Enter note name:")
                if not ok or not note_name:
                    return
                self.tabs_widget.setTabText(self.tabs_widget.currentIndex(), note_name)

            filename = os.path.join(self.predefined_folder, f"{note_name}.txt")
            with open(filename, 'w') as f:
                text = current_tab.toPlainText()
                f.write(text)
    def save_as_file(self):
        current_tab = self.tabs_widget.currentWidget()
        if current_tab:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            filename, _ = QFileDialog.getSaveFileName(self, "Save As", self.predefined_folder, 
                                                      "Text Files (*.txt);;Word Files (*.docx);;All Files (*)", options=options)
            if filename:
                # Ensure the file is saved in the predefined folder
                if not filename.startswith(self.predefined_folder):
                    QMessageBox.warning(self, "Warning", "Cascade's Notepad won't be able to detect these notes if you choose to save it to another directory than specified.")
                    return
                
                # Extract file extension
                file_extension = os.path.splitext(filename)[1].lower()

                # Save based on file extension
                if file_extension == ".txt":
                    with open(filename, 'w') as f:
                        text = current_tab.toPlainText()
                        f.write(text)
                elif file_extension == ".docx":
                    self.save_as_word(filename, current_tab.toPlainText())
                else:
                    with open(filename, 'w') as f:
                        text = current_tab.toPlainText()
                        f.write(text)

    def save_as_word(self, filename, text):
        from docx import Document

        doc = Document()
        doc.add_paragraph(text)
        doc.save(filename)

    def open_file(self, file_path=None):
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                # Create new tab and set content
                new_tab = QTextEdit(self)
                new_tab.setStyleSheet("background-color: #a791cb;")
                self.tabs.append(new_tab)
                index = self.tabs_widget.addTab(new_tab, "Untitled") 
                self.tabs_widget.setCurrentIndex(index)

                new_tab.setPlainText(content)  
                note_name = os.path.basename(file_path).rsplit('.', 1)[0]
                self.tabs_widget.setTabText(index, note_name)

            except FileNotFoundError:
                print(f"File not found: {file_path}")


    def find_text(self):
        text, ok = QInputDialog.getText(self, 'Find', 'Enter text to find:')
        if ok and text:
            cursor = self.central_widget.textCursor()
            cursor.movePosition(QTextCursor.Start)
            while cursor.find(text, QTextDocument.FindFlags()):
                pass

    def find_next(self):
        text, ok = QInputDialog.getText(self, 'Find Next', 'Enter text to find:')
        if ok and text:
            cursor = self.central_widget.textCursor()
            cursor.movePosition(QTextCursor.Down)
            cursor = self.central_widget.document().find(text, cursor)

    def find_prev(self):
        text, ok = QInputDialog.getText(self, 'Find Previous', 'Enter text to find:')
        if ok and text:
            cursor = self.central_widget.textCursor()
            cursor.movePosition(QTextCursor.Up)
            cursor = self.central_widget.document().find(text, cursor, QTextDocument.FindBackward)

    def replace_text(self):
        replace_dialog = ReplaceDialog(self)
        if replace_dialog.exec_() == QDialog.Accepted:
            find_text, replace_with = replace_dialog.get_inputs()
            if find_text:
                cursor = self.central_widget.textCursor()
                cursor.beginEditBlock()
                doc = self.central_widget.document()
                found = cursor.find(find_text)
                while found:
                    cursor.insertText(replace_with)
                    found = cursor.find(find_text)
                cursor.endEditBlock()
                
    def rename_file(self):
        current_tab = self.tabs_widget.currentWidget()
        if current_tab:
            old_note_name = self.tabs_widget.tabText(self.tabs_widget.currentIndex())
            if old_note_name == "Untitled":
                # Save the file if it is not saved before renaming
                self.save_file()
                old_note_name = self.tabs_widget.tabText(self.tabs_widget.currentIndex())

            new_note_name, ok = QInputDialog.getText(self, "Rename Note", "New name:", text=old_note_name)
            if ok and new_note_name:
                old_path = os.path.join(self.predefined_folder, f"{old_note_name}.txt")
                new_path = os.path.join(self.predefined_folder, f"{new_note_name}.txt")
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                self.tabs_widget.setTabText(self.tabs_widget.currentIndex(), new_note_name)

    def go_to(self):
        line_num, ok = QInputDialog.getInt(self, 'Go To Line', 'Enter line number:')
        if ok:
            cursor = self.central_widget.textCursor()
            cursor.movePosition(QTextCursor.Start)
            cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, line_num - 1)
            self.central_widget.setTextCursor(cursor)

    def change_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.central_widget.setFont(font)

    def zoom_in(self):
        self.central_widget.zoomIn(1)

    def zoom_out(self):
        self.central_widget.zoomOut(1)

    def toggle_word_wrap(self):
        if self.central_widget.lineWrapMode() == QTextEdit.WidgetWidth:
            self.central_widget.setLineWrapMode(QTextEdit.NoWrap)
        else:
            self.central_widget.setLineWrapMode(QTextEdit.WidgetWidth)

    def toggle_status_bar(self):
        if self.status_bar.isVisible():
            self.status_bar.hide()
        else:
            self.status_bar.show()

    def new_tab(self, file_path=None):
        new_tab = QTextEdit(self)
        new_tab.setStyleSheet("background-color: #a791cb;")
        self.tabs.append(new_tab)
        index = self.tabs_widget.addTab(new_tab, "Untitled")
        self.tabs_widget.setCurrentIndex(index)
        if file_path:
            with open(file_path, 'r') as f:
                content = f.read()
                new_tab.setPlainText(content)
            note_name = os.path.basename(file_path).rsplit('.', 1)[0]
            self.tabs_widget.setTabText(index, note_name)


    def new_window(self):
        new_window = Notepad()
        self.child_windows.append(new_window)
        new_window.show()

    def close_window(self):
        if len(self.tabs) == 1:
            self.close()
        else:
            self.child_windows.remove(self)
            self.deleteLater()

    def close_tab(self, index):
        if len(self.tabs) > 1:
            self.tabs.pop(index)
            self.tabs_widget.removeTab(index)
        else:
            QMessageBox.warning(self, 'Warning', 'Cannot close last tab.')

def main():
    app = QApplication(sys.argv)
    window = Notepad()
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        window.open_file(file_path)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
