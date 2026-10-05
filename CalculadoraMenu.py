# -*- coding: utf-8 -*-
"""
Calculadora simple (PySide6) con menú
--------------------------------------
Permite sumar, restar, multiplicar y dividir.
Controla la división entre cero y muestra el historial
de las últimas cinco operaciones.
Menú: "Calculadora" y "Acerca de...".
Creado por Jhudith Romero - 2026
"""

import sys
from collections import deque

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QMenu,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
)
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtCore import Qt

# ---------------------------------------------------------------------------
# Paleta de color rosado suave
# ---------------------------------------------------------------------------
COLOR_FONDO = "#FBEEEF"
COLOR_PANEL = "#F6DEE3"
COLOR_ACENTO = "#D9A5B3"
COLOR_BOTON = "#E4B7C2"
COLOR_BOTON_HOVER = "#D9A0B0"
COLOR_TEXTO = "#6B4B57"
COLOR_BLANCO = "#FFF9FA"

ESTILO = f"""
QMainWindow, QDialog {{
    background-color: {COLOR_FONDO};
}}
QWidget {{
    color: {COLOR_TEXTO};
    font-size: 13px;
}}
QMenuBar {{
    background-color: {COLOR_PANEL};
    color: {COLOR_TEXTO};
    font-weight: bold;
    padding: 4px;
}}
QMenuBar::item:selected {{
    background-color: {COLOR_ACENTO};
    border-radius: 4px;
}}
QMenu {{
    background-color: {COLOR_BLANCO};
    color: {COLOR_TEXTO};
    border: 1px solid {COLOR_ACENTO};
    border-radius: 6px;
    padding: 4px;
}}
QMenu::item:selected {{
    background-color: {COLOR_PANEL};
    border-radius: 4px;
}}
QLineEdit {{
    background-color: {COLOR_BLANCO};
    border: 1px solid {COLOR_ACENTO};
    border-radius: 6px;
    padding: 8px;
    font-size: 22px;
}}
QPushButton {{
    background-color: {COLOR_BOTON};
    color: {COLOR_TEXTO};
    border: none;
    border-radius: 8px;
    padding: 12px;
    font-weight: bold;
    font-size: 15px;
    min-width: 56px;
    min-height: 40px;
}}
QPushButton:hover {{
    background-color: {COLOR_BOTON_HOVER};
}}
QListWidget {{
    background-color: {COLOR_BLANCO};
    border: 1px solid {COLOR_ACENTO};
    border-radius: 6px;
    padding: 4px;
}}
"""


class DialogoAcercaDe(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de...")
        self.setMinimumWidth(340)

        titulo = QLabel("Calculadora Simple")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet(
            f"font-size: 16px; font-weight: bold; background-color: {COLOR_PANEL}; "
            "border-radius: 8px; padding: 8px;"
        )

        info = QLabel("Creado por Jhudith Romero - 2026\n\n"
                      "Aplicación con PySide6: sumar, restar, multiplicar y dividir.")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        botones.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addWidget(info)
        layout.addWidget(botones)
        self.setLayout(layout)


class Calculadora(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora")
        self.resize(420, 620)

        self.historial = deque(maxlen=5)
        self.operando = None
        self.operacion = None
        self.nuevo_numero = True

        # ---------------- Menú ----------------
        barra = self.menuBar()

        menu_calc = QMenu("Calculadora", self)
        accion_limpiar = QAction("Limpiar", self)
        accion_limpiar.setShortcut(QKeySequence("Ctrl+L"))
        accion_limpiar.triggered.connect(self.limpiar)
        accion_salir = QAction("Salir", self)
        accion_salir.setShortcut(QKeySequence("Ctrl+Q"))
        accion_salir.triggered.connect(self.close)
        menu_calc.addAction(accion_limpiar)
        menu_calc.addSeparator()
        menu_calc.addAction(accion_salir)

        menu_ayuda = QMenu("Acerca de...", self)
        accion_acerca = QAction("Acerca de...", self)
        accion_acerca.setShortcut(QKeySequence("F1"))
        accion_acerca.triggered.connect(self.mostrar_acerca_de)
        menu_ayuda.addAction(accion_acerca)

        barra.addMenu(menu_calc)
        barra.addMenu(menu_ayuda)

        # ---------------- Contenido ----------------
        central = QWidget()
        self.setCentralWidget(central)

        titulo = QLabel("Calculadora Simple")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet(
            f"font-size: 18px; font-weight: bold; background-color: {COLOR_PANEL}; "
            "border-radius: 8px; padding: 10px;"
        )

        self.pantalla = QLineEdit()
        self.pantalla.setReadOnly(True)
        self.pantalla.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.pantalla.setText("0")

        teclas = QGridLayout()
        botones = [
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["C", "⌫", "%", "±"],
        ]
        for fila_idx, fila in enumerate(botones):
            for col_idx, texto in enumerate(fila):
                boton = QPushButton(texto)
                boton.clicked.connect(lambda checked=False, t=texto: self.pulsar(t))
                teclas.addWidget(boton, fila_idx, col_idx)

        etiqueta_hist = QLabel("Historial (últimas 5 operaciones):")
        self.lista_historial = QListWidget()

        pie = QLabel("Creado por Jhudith Romero - 2026")
        pie.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pie.setStyleSheet(
            f"background-color: {COLOR_PANEL}; border-radius: 8px; "
            "padding: 6px; font-style: italic;"
        )

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addWidget(self.pantalla)
        layout.addLayout(teclas)
        layout.addWidget(etiqueta_hist)
        layout.addWidget(self.lista_historial)
        layout.addWidget(pie)
        central.setLayout(layout)

    # --------------------------- Ventanas ---------------------------
    def mostrar_acerca_de(self):
        DialogoAcercaDe(self).exec()

    # --------------------------- Lógica ---------------------------
    def pulsar(self, texto):
        if texto.isdigit():
            self.escribir_digito(texto)
        elif texto == ".":
            self.escribir_punto()
        elif texto == "C":
            self.limpiar()
        elif texto == "⌫":
            actual = self.pantalla.text()
            self.pantalla.setText(actual[:-1] if len(actual) > 1 else "0")
        elif texto == "%":
            self.pantalla.setText(self.formatear(float(self.pantalla.text()) / 100))
        elif texto == "±":
            valor = float(self.pantalla.text())
            self.pantalla.setText(self.formatear(-valor))
        elif texto == "=":
            self.calcular()
        else:  # operadores
            self.guardar_operando(texto)

    def escribir_digito(self, digito):
        if self.nuevo_numero:
            self.pantalla.setText(digito)
            self.nuevo_numero = False
        else:
            actual = self.pantalla.text()
            self.pantalla.setText(digito if actual == "0" else actual + digito)

    def escribir_punto(self):
        if self.nuevo_numero:
            self.pantalla.setText("0.")
            self.nuevo_numero = False
        elif "." not in self.pantalla.text():
            self.pantalla.setText(self.pantalla.text() + ".")

    def guardar_operando(self, simbolo):
        if self.operacion is not None and not self.nuevo_numero:
            self.calcular()
        self.operando = float(self.pantalla.text())
        self.operacion = simbolo
        self.nuevo_numero = True

    def calcular(self):
        if self.operacion is None or self.operando is None:
            return
        try:
            b = float(self.pantalla.text())
        except ValueError:
            return

        a = self.operando
        if self.operacion == "+":
            resultado = a + b
        elif self.operacion == "-":
            resultado = a - b
        elif self.operacion == "×":
            resultado = a * b
        else:  # ÷
            if b == 0:
                QMessageBox.critical(self, "Error", "No se puede dividir entre cero.")
                self.limpiar()
                return
            resultado = a / b

        self.pantalla.setText(self.formatear(resultado))
        self.historial.appendleft(
            f"{self.formatear(a)} {self.operacion} {self.formatear(b)} = {self.formatear(resultado)}"
        )
        self.lista_historial.clear()
        self.lista_historial.addItems(self.historial)

        self.operando = None
        self.operacion = None
        self.nuevo_numero = True

    def limpiar(self):
        self.pantalla.setText("0")
        self.operando = None
        self.operacion = None
        self.nuevo_numero = True

    @staticmethod
    def formatear(valor):
        return str(int(valor)) if isinstance(valor, float) and valor == int(valor) else str(valor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(ESTILO)
    ventana = Calculadora()
    ventana.show()
    sys.exit(app.exec())
