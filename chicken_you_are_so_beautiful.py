#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import getpass
import time
import darkdetect
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QCheckBox, QTextEdit, QFormLayout, QHBoxLayout, QWidget, \
    QMainWindow, QApplication, QMessageBox
import qtawesome as qta
from qt_material import *


class ChickenYouSoBeautiful(QMainWindow, QtStyleTools):
    def __init__(self):
        super().__init__()
        # 获取屏幕分辨率
        x = QApplication.primaryScreen().size().width()
        y = QApplication.primaryScreen().size().height()
        self.setWindowTitle("鸡你太美")
        self.setFixedSize(x // 2, y // 2)
        # 设置图标
        self.setWindowIcon(QIcon("image/ikun.ico"))
        # 设置窗口位置为屏幕中心
        self.move(x // 2 - self.width() // 2, y // 2 - self.height() // 2)
        # 设置窗口置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.message_sequence = [
            '鸡你', 'Oh Baby', '多一眼就会爆炸',
            '鸡你', 'Oh Baby', '多一眼就会爆炸',
            '干嘛', 'Oh Magi', '多一眼就会爆炸'
        ]
        self.user_sequence = []
        # 设置窗口布局为表单布局
        self.form_layout = QFormLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.form_layout)
        self.setCentralWidget(self.central_widget)
        # 添加一个多行文本框
        self.text_edit = QTextEdit()
        self.form_layout.addRow(self.text_edit)
        # 设置多行文本框为只读
        self.text_edit.setReadOnly(True)
        # 添加一个水平布局，放置单行文本框和按钮
        self.h_layout = QHBoxLayout()
        self.form_layout.addRow(self.h_layout)
        # 添加一个单行文本框
        self.line_edit = QLineEdit()
        self.h_layout.addWidget(self.line_edit)
        # 添加一个按钮
        self.button = QPushButton("发送")
        # 设置按钮图标(使用FontAwesome 4.7.0)
        self.button.setIcon(qta.icon("fa5s.keyboard"))
        # 禁用按钮
        self.button.setEnabled(False)
        self.h_layout.addWidget(self.button)
        # 新建一个水平布局，放置两个复选框
        self.h_layout_check_box = QHBoxLayout()
        self.form_layout.addRow(self.h_layout_check_box)
        # 新建一个单选框，用于选择是否开启文字自动补全
        self.check_box = QCheckBox("开启文字自动补全")
        self.h_layout_check_box.addWidget(self.check_box)
        # 新建一个复选框，用于选择是否开启暗黑模式
        self.check_box_dark = QCheckBox("开启暗黑模式")
        self.h_layout_check_box.addWidget(self.check_box_dark)
        # 为复选框添加状态改变事件
        self.check_box_dark.stateChanged.connect(self.dark_mode)
        # 判断当前系统是否为暗黑模式
        if darkdetect.isDark():
            self.check_box_dark.setChecked(True)
        hyperlink_web = '<a href="https://senge.dev">点此访问个人博客</a>'
        hyperlink_bilibili = '<a href="https://space.bilibili.com/151336873">点此访问B站主页</a>'
        hyperlink_video = '<a href="https://www.bilibili.com/video/BV1Q44y1o77h">原视频链接</a>'
        self.label = QLabel(f"作者：森哥Dev\t{hyperlink_web}\t{hyperlink_bilibili}\t{hyperlink_video}")
        self.label.setOpenExternalLinks(True)
        self.form_layout.addRow(self.label)
        # 为按钮添加点击事件
        self.button.clicked.connect(self.send_message)
        # 为单行文本框添加回车事件
        self.line_edit.returnPressed.connect(self.send_message)
        # 为单行文本框添加内容改变事件
        self.line_edit.textChanged.connect(self.text_changed)
        # 将程序的焦点设置到单行文本框
        self.line_edit.setFocus()

    def dark_mode(self):
        # 判断复选框是否被选中
        if self.check_box_dark.isChecked():
            # 设置程序的样式表
            self.apply_stylesheet(self, 'dark_cyan.xml')
        else:
            # 设置程序的样式表
            self.apply_stylesheet(self, 'light_cyan.xml')

    def text_changed(self):
        # 判断单行文本框的内容是否为空
        if self.line_edit.text() == "":
            # 禁用发送按钮
            self.button.setEnabled(False)
            return
        else:
            # 启用发送按钮
            self.button.setEnabled(True)
        # 判断是否开启文字自动补全
        if not self.check_box.isChecked():
            return
        # 判断单行文本的第一个字
        if self.line_edit.text()[0] == "鸡" or self.line_edit.text()[0].upper() == 'J':
            self.line_edit.setText("鸡你")
            self.line_edit.setCursorPosition(len(self.line_edit.text()))
        elif self.line_edit.text()[0] == "多" or self.line_edit.text()[0].upper() == "D":
            self.line_edit.setText("多一眼就会爆炸")
            self.line_edit.setCursorPosition(len(self.line_edit.text()))
        elif self.line_edit.text()[0] == "干" or self.line_edit.text()[0].upper() == "G":
            self.line_edit.setText("干嘛")
            self.line_edit.setCursorPosition(len(self.line_edit.text()))
        elif self.line_edit.text()[0].upper() == "B":
            self.line_edit.setText("Oh Baby")
            self.line_edit.setCursorPosition(len(self.line_edit.text()))
        elif self.line_edit.text()[0].upper() == "M":
            self.line_edit.setText("Oh Magi")
            self.line_edit.setCursorPosition(len(self.line_edit.text()))

    def send_message(self):
        # 获取单行文本框的内容
        message = self.line_edit.text()
        if message == "":
            QMessageBox.warning(self, "绿尸寒警告", "小黑子，食不食油饼？")
            return
        message_dict = {
            "鸡你": "实在太美",
            "Oh Baby": "实在是太美",
            "多一眼就会爆炸": "近一点快被融化",
            "干嘛": "干嘛哈嗨呦",
            "Oh Magi": "哦呀哈哈哟"
        }
        # 判断单行文本框的内容是否在字典中
        message_ = message_dict[message] if message in message_dict else "对接失败"
        # 将单行文本框的内容添加到多行文本框中
        self.text_edit.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{getpass.getuser()}：\n{message}\n")
        # 禁用单行文本框
        self.line_edit.setEnabled(False)
        # 清空单行文本框
        self.line_edit.clear()
        # 将聊天内容保存到user_sequence中
        self.user_sequence.append(message)
        length = len(self.user_sequence)
        # 截取self.message_sequence中的前length个元素
        message_sequence = self.message_sequence[:length]
        # 将窗口标题改为对方正在输入...
        self.setWindowTitle("对方正在输入...")

        # 判断二者是否相等
        if self.user_sequence == message_sequence:
            # 为定时器添加超时事件
            delay = len(message_) * 200
            QTimer.singleShot(delay, lambda: self.timer(message_))
            if self.user_sequence == self.message_sequence:
                # 清除user_sequence中的内容
                self.user_sequence = []
                choice = QMessageBox.information(self, "提示", "对接成功，是否清除聊天记录？",
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if choice == QMessageBox.Yes:
                    # 清除多行文本框中的内容
                    self.text_edit.clear()
        else:
            for item in range(len(self.user_sequence)):
                if self.user_sequence[item] != message_sequence[item]:
                    # 清除user_sequence中的内容
                    self.user_sequence = []
                    # 清除多行文本框中的内容
                    self.text_edit.clear()
                    # 清除单行文本框中的内容
                    self.line_edit.clear()
                    # 启动单行文本框
                    self.line_edit.setEnabled(True)
                    # 重新设置焦点
                    self.line_edit.setFocus()
                    # 弹窗提示
                    QMessageBox.critical(self, "错误", "对接失败！")
                    # 重新设置窗口标题
                    self.setWindowTitle("鸡你太美")

    def timer(self, message):
        # 将窗口标题改为聊天窗口
        self.setWindowTitle("鸡你太美")
        # 发送机器人回复
        self.text_edit.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t纯鹿人：\n{message}\n")
        # 启用单行文本框
        self.line_edit.setEnabled(True)
        # 将焦点设置到单行文本框
        self.line_edit.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置主题
    app.setApplicationName("鸡你太美")
    # 设置Qt Material主题
    if darkdetect.isDark():
        apply_stylesheet(app, theme="dark_cyan.xml")
    else:
        apply_stylesheet(app, theme="light_cyan.xml")
    window = ChickenYouSoBeautiful()
    window.show()
    sys.exit(app.exec())
