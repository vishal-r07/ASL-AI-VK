#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main Window for ASL Translator and Emotion Communicator

This module contains the MainWindow class which is the primary GUI component
for the application, featuring a modern, polished interface.
"""

import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTextEdit, QComboBox,
    QAction, QMenu, QMenuBar, QStatusBar, QTabWidget,
    QSplitter, QFrame, QFileDialog, QMessageBox, QGroupBox
)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage
import cv2

# Import our modules
from src.asl.detector_optimized import OptimizedASLDetector
from src.emotion.detector import EmotionDetector
from src.utils.camera import Camera
from src.history.manager import HistoryManager
from src.gui.about_dialog import AboutDialog
from src.gui.help_dialog import HelpDialog
from src.utils.text_to_speech import TextToSpeech
from src.utils.prediction_enhancer import PredictionEnhancer

class MainWindow(QMainWindow):
    """Main window for the ASL Translator and Emotion Communicator application."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.camera = Camera()
        # Set mirror_output=False for correct hand orientation (not selfie-mirrored)
        self.asl_detector = OptimizedASLDetector(mirror_output=False)
        self.emotion_detector = EmotionDetector()
        self.history_manager = HistoryManager()
        self.text_to_speech = TextToSpeech()
        
        mapping_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                                   "data", "word_emotion_mapping.json")
        self.prediction_enhancer = PredictionEnhancer(mapping_file)
        
        self.init_ui()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        
        self.current_asl_text = ""
        self.current_emotion = ""
        self.is_recording = False
        self.text_to_speech_enabled = False
        self.last_spoken_text = ""
    
    def init_ui(self):
        """Initialize the user interface with a modern look."""
        self.setWindowTitle("ASL Translator and Emotion Communicator")
        self.setGeometry(100, 100, 1280, 720)
        self.setStyleSheet(self.get_stylesheet())
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        splitter = QSplitter(Qt.Horizontal)
        
        left_panel = self.create_left_panel()
        right_panel = self.create_right_panel()
        
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([800, 480])
        
        main_layout.addWidget(splitter)
        
        self.create_menu_bar()
        self.statusBar().showMessage("Ready")

    def create_left_panel(self):
        """Creates the left panel containing the camera feed and controls."""
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Camera Feed Box
        camera_group = QGroupBox("Camera Feed")
        camera_layout = QVBoxLayout(camera_group)
        self.camera_label = QLabel("Initializing Camera...")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setObjectName("cameraLabel")
        camera_layout.addWidget(self.camera_label)
        left_layout.addWidget(camera_group)

        # Controls Box
        controls_group = QGroupBox("Controls")
        controls_layout = QVBoxLayout(controls_group)
        
        # Camera and Recording Controls
        cam_rec_layout = QHBoxLayout()
        self.camera_button = QPushButton("Stop Camera")
        self.camera_button.clicked.connect(self.toggle_camera)
        self.record_button = QPushButton("Start Recording")
        self.record_button.clicked.connect(self.toggle_recording)
        cam_rec_layout.addWidget(self.camera_button)
        cam_rec_layout.addWidget(self.record_button)
        controls_layout.addLayout(cam_rec_layout)

        # Voice Reply Controls
        tts_layout = QHBoxLayout()
        self.tts_button = QPushButton("Enable Voice Reply")
        self.tts_button.setCheckable(True)
        self.tts_button.clicked.connect(self.toggle_text_to_speech)
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Hindi"])
        tts_layout.addWidget(self.tts_button)
        tts_layout.addWidget(self.language_combo)
        controls_layout.addLayout(tts_layout)

        left_layout.addWidget(controls_group)
        return left_panel

    def create_right_panel(self):
        """Creates the right panel containing the translation and history tabs."""
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        tabs = QTabWidget()

        # Live Translation Tab
        translation_tab = QWidget()
        translation_layout = QVBoxLayout(translation_tab)
        asl_group = QGroupBox("ASL Translation")
        asl_layout = QVBoxLayout(asl_group)
        self.asl_text = QTextEdit()
        self.asl_text.setReadOnly(True)
        self.asl_text.setObjectName("aslText")
        self.asl_text.setWordWrapMode(True)
        self.asl_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.asl_text.setStyleSheet("padding: 12px; margin: 6px; border-radius: 8px; background: #3B4252; font-size: 22pt; font-weight: bold; color: #A3BE8C;")
        asl_layout.addWidget(self.asl_text)
        emotion_group = QGroupBox("Detected Emotion")
        emotion_layout = QVBoxLayout(emotion_group)
        self.emotion_text = QTextEdit()
        self.emotion_text.setReadOnly(True)
        self.emotion_text.setObjectName("emotionText")
        self.emotion_text.setWordWrapMode(True)
        self.emotion_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.emotion_text.setStyleSheet("padding: 10px; margin: 6px; border-radius: 8px; background: #3B4252; font-size: 18pt; color: #B48EAD;")
        emotion_layout.addWidget(self.emotion_text)
        translation_layout.addWidget(asl_group)
        translation_layout.addWidget(emotion_group)
        translation_tab.setLayout(translation_layout)

        # History Tab
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)
        history_group = QGroupBox("Translation History")
        history_group_layout = QVBoxLayout(history_group)
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        history_group_layout.addWidget(self.history_text)
        history_controls_layout = QHBoxLayout()
        clear_history_button = QPushButton("Clear History")
        clear_history_button.clicked.connect(self.clear_history)
        save_history_button = QPushButton("Save History")
        save_history_button.clicked.connect(self.save_history)
        history_controls_layout.addWidget(clear_history_button)
        history_controls_layout.addWidget(save_history_button)
        history_group_layout.addLayout(history_controls_layout)
        history_layout.addWidget(history_group)
        history_tab.setLayout(history_layout)

        tabs.addTab(translation_tab, "Live Translation")
        tabs.addTab(history_tab, "History")
        right_layout.addWidget(tabs)
        return right_panel

    def create_menu_bar(self):
        """Create the menu bar with actions."""
        file_menu = self.menuBar().addMenu("&File")
        save_action = QAction("&Save History", self, shortcut="Ctrl+S", triggered=self.save_history)
        exit_action = QAction("&Exit", self, shortcut="Ctrl+Q", triggered=self.close)
        file_menu.addActions([save_action, exit_action])

        settings_menu = self.menuBar().addMenu("&Settings")
        camera_action = QAction("&Camera Settings", self, triggered=self.open_camera_settings)
        settings_menu.addAction(camera_action)

        help_menu = self.menuBar().addMenu("&Help")
        help_action = QAction("&Help", self, shortcut="F1", triggered=self.show_help_dialog)
        about_action = QAction("&About", self, triggered=self.show_about_dialog)
        help_menu.addActions([help_action, about_action])

    def update_frame(self):
        """Update and process the camera frame."""
        ret, frame = self.camera.get_frame()
        if not ret:
            return

        emotion_result = self.emotion_detector.process_frame(frame, self.current_asl_text, self.prediction_enhancer)
        if emotion_result:
            self.current_emotion = emotion_result
            self.emotion_text.setText(self.current_emotion)

        asl_result, annotated_frame = self.asl_detector.process_frame(frame)
        if asl_result:
            self.current_asl_text = asl_result
            self.asl_text.setText(self.current_asl_text)
            if self.is_recording:
                self.history_manager.add_entry(self.current_asl_text, self.current_emotion)
                self.update_history_display()
            if self.text_to_speech_enabled:
                self.speak_text(self.current_asl_text)
        
        self.display_frame(annotated_frame)

    def display_frame(self, frame):
        """Displays a frame in the camera label."""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.camera_label.setPixmap(pixmap.scaled(self.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def toggle_camera(self):
        """Toggle the camera on/off."""
        if self.timer.isActive():
            self.timer.stop()
            self.camera_button.setText("Start Camera")
            self.camera_label.setText("Camera Stopped")
            self.camera_label.setPixmap(QPixmap())
        else:
            self.timer.start(30)
            self.camera_button.setText("Stop Camera")

    def toggle_recording(self):
        """Toggle recording of translations."""
        self.is_recording = not self.is_recording
        self.record_button.setText("Stop Recording" if self.is_recording else "Start Recording")
        self.statusBar().showMessage("Recording started" if self.is_recording else "Recording stopped")

    def toggle_text_to_speech(self, checked):
        """Toggle text-to-speech functionality."""
        self.text_to_speech_enabled = checked
        self.tts_button.setText("Disable Voice Reply" if checked else "Enable Voice Reply")
        self.statusBar().showMessage("Voice Reply enabled" if checked else "Voice Reply disabled")

    def speak_text(self, text):
        """Speak the given text using text-to-speech in the selected language."""
        if text != self.last_spoken_text:
            lang_map = {"English": "en", "Hindi": "hi"}
            language = lang_map.get(self.language_combo.currentText(), 'en')
            # Auto-translate to Hindi if Hindi is selected
            if language == 'hi':
                try:
                    from googletrans import Translator
                    translator = Translator()
                    translated = translator.translate(text, src='en', dest='hi')
                    text = translated.text
                except Exception as e:
                    print(f"Translation error: {e}")
            self.text_to_speech.speak(text, lang=language)
            self.last_spoken_text = text

    def update_history_display(self):
        """Update the history display with the latest entries."""
        self.history_text.clear()
        for entry in self.history_manager.get_entries():
            formatted_entry = f'[{entry["timestamp"]}] ASL: {entry["asl_text"]} | Emotion: {entry["emotion"]}\n'
            self.history_text.append(formatted_entry)

    def clear_history(self):
        """Clear the translation history."""
        self.history_manager.clear_entries()
        self.update_history_display()
        self.statusBar().showMessage("History cleared")

    def save_history(self):
        """Save the translation history to a file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save History", "", "Text Files (*.txt);;All Files (*)")
        if file_path and self.history_manager.save_to_file(file_path):
            self.statusBar().showMessage(f"History saved to {file_path}")
        elif file_path:
            QMessageBox.warning(self, "Save Error", "Failed to save history.")

    def open_camera_settings(self):
        """Open camera settings dialog."""
        QMessageBox.information(self, "Camera Settings", "Camera settings not yet implemented.")

    def show_about_dialog(self):
        """Show the about dialog."""
        AboutDialog(self).exec_()

    def show_help_dialog(self):
        """Show the help dialog."""
        HelpDialog(self).exec_()

    def closeEvent(self, event):
        """Handle the window close event."""
        self.timer.stop()
        if self.camera.cap:
            self.camera.cap.release()
        event.accept()

    def get_stylesheet(self):
        """Returns the stylesheet for the application."""
        return """
            QMainWindow, QWidget {
                background-color: #2E3440;
                color: #D8DEE9;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                font-size: 12pt;
                font-weight: bold;
                color: #88C0D0;
                border: 1px solid #4C566A;
                border-radius: 5px;
                margin-top: 1ex; 
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
            #cameraLabel {
                background-color: #3B4252;
                border: 1px solid #4C566A;
                border-radius: 5px;
            }
            QTextEdit {
                background-color: #3B4252;
                border: 1px solid #4C566A;
                border-radius: 5px;
                color: #ECEFF4;
                font-size: 11pt;
            }
            #aslText {
                font-size: 20pt;
                font-weight: bold;
                color: #A3BE8C;
            }
            #emotionText {
                font-size: 16pt;
                color: #B48EAD;
            }
            QPushButton {
                background-color: #5E81AC;
                color: #ECEFF4;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
            QPushButton:pressed, QPushButton:checked {
                background-color: #88C0D0;
            }
            QComboBox {
                background-color: #434C5E;
                border: 1px solid #4C566A;
                border-radius: 4px;
                padding: 4px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QTabWidget::pane {
                border: 1px solid #4C566A;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #434C5E;
                padding: 8px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #5E81AC;
            }
            QMenuBar {
                background-color: #3B4252;
            }
            QMenu {
                background-color: #3B4252;
            }
            QStatusBar {
                color: #D8DEE9;
            }
        """