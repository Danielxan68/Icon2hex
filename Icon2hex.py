import sys
import binascii
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QFont
import icon_data
import os

class IconConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Imposta l'icona dell'applicazione
        icon_data_bytes = binascii.unhexlify(icon_data.icon_hex_data.replace("\n", "").replace(" ", ""))
        pixmap = QPixmap()
        pixmap.loadFromData(icon_data_bytes)
        self.setWindowIcon(QIcon(pixmap))

        # Imposta il font dell'interfaccia grafica
        self.setFont(QFont("Arial", 13))

        self.sourceFileEdit = QLineEdit(self)
        self.sourceFileEdit.setPlaceholderText("Seleziona il file sorgente")
        self.sourceFileEdit.setReadOnly(True)
        self.sourceFileEdit.mousePressEvent = self.showDialog
        self.layout.addWidget(self.sourceFileEdit)

        self.fileNameEdit = QLineEdit(self)
        self.fileNameEdit.setPlaceholderText("Nome del file generato .py")
        self.layout.addWidget(self.fileNameEdit)

        self.convertBtn = QPushButton("Converti Icona", self)
        self.convertBtn.clicked.connect(self.convertIconToHex)
        self.convertBtn.setStyleSheet("""
            QPushButton {
                background-color: #FF8000;
                color: white;
                border-radius: 5px;
                font: 20pt "Arial";
            }
            QPushButton:hover {
                background-color: #FF5000;
            }
        """)
        self.layout.addWidget(self.convertBtn)

        self.setLayout(self.layout)
        self.setWindowTitle('Icon Converter')
        self.setMinimumSize(400, 150)  # Imposta la dimensione minima della finestra
        self.show()

    def showDialog(self, event):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Seleziona un'icona", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if fileName:
            self.sourceFileEdit.setText(fileName)
            default_output_file_name = os.path.splitext(os.path.basename(fileName))[0] + ".py"
            self.fileNameEdit.setText(default_output_file_name)

    def convertIconToHex(self):
        file_path = self.sourceFileEdit.text()
        if not file_path:
            QMessageBox.information(self, "Icon Converter", "Per favore, seleziona un file sorgente.")
            return

        output_file_name = self.fileNameEdit.text()
        if not output_file_name:
            QMessageBox.information(self, "Icon Converter", "Per favore, specifica il nome del file di output.")
            return

        with open(file_path, "rb") as image_file:
            binary_data = image_file.read()

        hex_data = binary_data.hex()

        icon_data_content = f"icon_hex_data = '{hex_data}'"

        folder_path = os.path.dirname(file_path)
        output_file_path = os.path.join(folder_path, output_file_name)

        with open(output_file_path, "w") as hex_file:
            hex_file.write(icon_data_content)

        QMessageBox.information(self, "Icon Converter", f"Dati esadecimali salvati in '{output_file_path}' per il file: {os.path.basename(file_path)}")
        return
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = IconConverter()
    sys.exit(app.exec_())
