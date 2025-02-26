#!/usr/bin/python3
# coding: utf-8

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QColor, QPalette
import kociemba

class RubiksCubeSolver(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("ルービックキューブ ソルバー")
        self.setGeometry(100, 100, 500, 600)

        layout = QVBoxLayout()

        self.label = QLabel("色を選択し、ボタンをクリックしてキューブの状態を設定してください:")
        layout.addWidget(self.label)

        self.color_map = {
            'U': "white", 'R': "red", 'F': "green",
            'D': "yellow", 'L': "blue", 'B': "orange"
        }
        self.current_color = 'U'
        self.color_label = QLabel(f"選択中の色: {self.current_color}")
        layout.addWidget(self.color_label)

        self.grid_layout = QGridLayout()
        self.buttons = []

        cube_layout = [
            [None, None, 'U', None, None],
            ['L', 'F', 'R', 'B', None],
            [None, None, 'D', None, None]
        ]
        
        for i, row in enumerate(cube_layout):
            for j, face in enumerate(row):
                if face:
                    face_buttons = []
                    face_layout = QGridLayout()
                    for r in range(3):
                        for c in range(3):
                            button = QPushButton('')
                            button.setFixedSize(40, 40)
                            button.setStyleSheet(f"background-color: {self.color_map[face]}")
                            button.clicked.connect(self.set_color)
                            face_layout.addWidget(button, r, c)
                            face_buttons.append(button)
                    self.grid_layout.addLayout(face_layout, i, j)
                    self.buttons.extend(face_buttons)
        
        layout.addLayout(self.grid_layout)

        self.color_buttons_layout = QHBoxLayout()
        for color, color_name in self.color_map.items():
            color_button = QPushButton(color)
            color_button.setStyleSheet(f"background-color: {color_name}")
            color_button.clicked.connect(self.change_color)
            self.color_buttons_layout.addWidget(color_button)

        layout.addLayout(self.color_buttons_layout)

        self.solve_button = QPushButton('解決', self)
        self.solve_button.clicked.connect(self.solve_cube)
        layout.addWidget(self.solve_button)

        self.solution_output = QTextEdit(self)
        self.solution_output.setReadOnly(True)
        layout.addWidget(self.solution_output)

        self.setLayout(layout)

    def change_color(self):
        sender = self.sender()
        self.current_color = sender.text()
        self.color_label.setText(f"選択中の色: {self.current_color}")

    def set_color(self):
        sender = self.sender()
        sender.setStyleSheet(f"background-color: {self.color_map[self.current_color]}")
        sender.setText(self.current_color)

    def solve_cube(self):
        cube_state = ''.join(button.text() if button.text() else 'U' for button in self.buttons)
        try:
            solution = kociemba.solve(cube_state)
            self.solution_output.setText(solution)
        except Exception as e:
            self.solution_output.setText(f'エラー: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    solver = RubiksCubeSolver()
    solver.show()
    sys.exit(app.exec_())
