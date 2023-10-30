from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from ui import Ui_MainWindow  # Replace 'ui' with the actual name of your generated file
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QByteArray, QBuffer
import cv2
import numpy as np
import os
import time
from registeration_pair import register_images
from registeration_sequence import main as registration_main
import sys
from PyQt5 import QtWidgets, QtCore


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fixed_image = None
        self.moving_image = None
        self.registered_image = None
        self.fixedimage.clicked.connect(self.load_fixed_image)
        self.movingimage.clicked.connect(self.load_moving_image)
        self.registerimage_2.clicked.connect(self.perform_registration)
        self.registerimage.clicked.connect(self.save_registered_image)
        
        self.registerimage_3.clicked.connect(self.select_input_folder)
        self.registerimage_5.clicked.connect(self.select_output_folder)
        self.registerimage_4.clicked.connect(self.run_registration)
        
        self.input_folder = ''
        self.output_folder = ''
        
    def select_input_folder(self):
        self.input_folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if self.input_folder:
            QtWidgets.QMessageBox.information(self, "Folder Selected", "Input folder has been selected successfully!")
        else:
            QtWidgets.QMessageBox.warning(self, "No Folder Selected", "No input folder was selected.")
        

    def select_output_folder(self):
        self.output_folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if self.output_folder:
            QtWidgets.QMessageBox.information(self, "Folder Selected", "Output folder has been selected successfully!")
        else:
            QtWidgets.QMessageBox.warning(self, "No Folder Selected", "No output folder was selected.")
        
    def run_registration(self):
        if not self.input_folder or not self.output_folder:
            QtWidgets.QMessageBox.warning(self, "Folders Not Set", "Please select both input and output folders before running the registration.")
            return

        self.set_interface_enabled(False)  # Disable the interface during processing
        QtWidgets.QMessageBox.information(self, "Process Started", "Image registration is in progress. This may take some time. Click on the OK button to continue. All features will be disabled during the process.")

        QtCore.QTimer.singleShot(100, self.start_registration_process)  # Start after a short delay to allow the message box to close
        
    def start_registration_process(self):
        try:
            registration_main(self.input_folder, self.output_folder)  # Call the modified main function from the backend script
            QtWidgets.QMessageBox.information(self, "Process Complete", "Image registration completed successfully!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred during registration: {e}")
        finally:
            self.set_interface_enabled(True)  # Re-enable the interface after processing
            
    def set_interface_enabled(self, enabled):
        # You would enable or disable the relevant interface components here
        self.registerimage_3.setEnabled(enabled)
        self.registerimage_5.setEnabled(enabled)
        self.registerimage_4.setEnabled(enabled)
            

    @pyqtSlot()
    def perform_registration(self):
        if self.fixed_image is None or self.moving_image is None:
            QMessageBox.warning(self, "Warning", "Please load both fixed and moving images first.")
            return
        
        # Perform registration
        start_time = time.time()
        self.registered_image, H = register_images(self.fixed_image, self.moving_image)
        end_time = time.time()
        QMessageBox.information(self, "Information", f"Registration completed in {end_time - start_time:.2f} seconds.")

        # Display the result in the image2 panel
        height, width = self.registered_image.shape[:2]
        bytesPerLine = 3 * width
        qImg = QImage(self.registered_image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qImg)
        self.image2.setPixmap(pixmap.scaled(self.image2.width(), self.image2.height(), Qt.KeepAspectRatio))
        
        # Convert the result to QImage and then to QPixmap for display
        try:
            height, width = self.registered_image.shape[:2]  # Works for both grayscale and color
            if len(self.registered_image.shape) == 3:
                bytesPerLine = 3 * width
                qImg = QImage(self.registered_image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            else:  # Grayscale
                bytesPerLine = width
                qImg = QImage(self.registered_image.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
            
            pixmap = QPixmap.fromImage(qImg)
            self.image2.setPixmap(pixmap.scaled(self.image2.width(), self.image2.height(), Qt.KeepAspectRatio))
        except AttributeError as e:
            QMessageBox.critical(self, "Error", "Failed to convert the registered image for display.\n" + str(e))
        
    def save_registered_image(self):
        if self.registered_image is None:
            QMessageBox.warning(self, "Warning", "No registered image to save. Please perform registration first.")
            return
        
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "TIFF Files (*.tif *.png *.jpg *.bmp);;All Files (*)")
        if fileName:
            cv2.imwrite(fileName, self.registered_image)
            QMessageBox.information(self, "Information", "Registered image saved successfully.")
        
    def load_fixed_image(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.tif *.png *.jpg *.bmp)")
        if fileName:
            image = cv2.imread(fileName, cv2.IMREAD_UNCHANGED)
            if image is None or image.dtype != np.uint8 or (image.shape[0] > 300 or image.shape[1] > 300):
                QMessageBox.warning(self, "Warning", "Please upload an 8-bit PNG image with dimensions up to 300x300.")
                return
            self.fixed_image = image
            pixmap = QPixmap(fileName)
            self.image3.setPixmap(pixmap.scaled(self.image3.width(), self.image3.height(), Qt.KeepAspectRatio))

    def load_moving_image(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.tif *.png *.jpg *.bmp)")
        if fileName:
            image = cv2.imread(fileName, cv2.IMREAD_UNCHANGED)
            if image is None or image.dtype != np.uint8 or (image.shape[0] > 300 or image.shape[1] > 300):
                QMessageBox.warning(self, "Warning", "Please upload an 8-bit PNG image with dimensions up to 300x300.")
                return
            self.moving_image = image
            pixmap = QPixmap(fileName)
            self.image1.setPixmap(pixmap.scaled(self.image1.width(), self.image1.height(), Qt.KeepAspectRatio))
            
            
class RegistrationThread(QThread):
    finished = pyqtSignal(np.ndarray, np.ndarray)  # Signal to indicate the registration is finished

    def __init__(self, img1, img2):
        QThread.__init__(self)
        self.img1 = img1
        self.img2 = img2

    def run(self):
        registered_image, H = register_images(self.img1, self.img2)
        self.finished.emit(registered_image, H)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet("QMessageBox { color: black; } QMessageBox QLabel { color: white; }")
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
