import sys
import requests
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                            QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, 
                            QMessageBox, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDateTime
from PyQt5.QtGui import QIcon, QFont  # 已包含QIcon导入

class UpdateThread(QThread):
    # 保持不变...
    """更新hosts的后台线程，避免界面卡顿"""
    log_signal = pyqtSignal(str)
    result_signal = pyqtSignal(bool)

    def run(self):
        try:
            # 获取最新hosts
            self.log_signal.emit("正在获取最新的Github hosts信息...")
            latest_hosts = self.get_latest_hosts()
            if not latest_hosts:
                self.result_signal.emit(False)
                return

            # 读取本地hosts
            self.log_signal.emit("正在读取本地hosts文件...")
            local_lines = self.read_local_hosts()
            if local_lines is None:
                self.result_signal.emit(False)
                return

            # 解析最新hosts
            github_hosts = self.parse_github_hosts(latest_hosts)
            if not github_hosts:
                self.log_signal.emit("未获取到有效的Github hosts信息")
                self.result_signal.emit(False)
                return

            # 构建新的hosts内容
            self.log_signal.emit("正在生成新的hosts内容...")
            new_lines = self.build_new_hosts(local_lines, github_hosts)
            if not new_lines:
                self.result_signal.emit(False)
                return

            # 写入更新后的内容
            self.log_signal.emit("正在更新hosts文件...")
            success = self.write_local_hosts(new_lines)
            self.result_signal.emit(success)

        except Exception as e:
            self.log_signal.emit(f"发生错误: {str(e)}")
            self.result_signal.emit(False)

    def get_latest_hosts(self):
        url = "https://raw.hellogithub.com/hosts.json"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.log_signal.emit(f"获取最新hosts失败: {e}")
            return None

    def read_local_hosts(self):
        if os.name == 'nt':
            hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        else:
            hosts_path = "/etc/hosts"
        
        try:
            with open(hosts_path, 'r', encoding='utf-8') as f:
                return f.readlines()
        except PermissionError:
            self.log_signal.emit("权限不足，无法读取hosts文件。请以管理员身份运行程序。")
            return None
        except Exception as e:
            self.log_signal.emit(f"读取hosts文件失败: {e}")
            return None

    def parse_github_hosts(self, latest_hosts):
        github_hosts = {}
        if isinstance(latest_hosts, list):
            for entry in latest_hosts:
                if isinstance(entry, list) and len(entry) >= 2:
                    ip = entry[0]
                    domain = entry[1]
                    if domain and ip:
                        github_hosts[domain] = ip
        else:
            self.log_signal.emit(f"未知的数据结构: {type(latest_hosts)}")
            return None
        return github_hosts

    def build_new_hosts(self, local_lines, github_hosts):
        start_marker = "# GitHub Hosts Start"
        end_marker = "# GitHub Hosts End"
        
        start_index = -1
        end_index = -1
        
        for i, line in enumerate(local_lines):
            if start_marker in line:
                start_index = i
            elif end_marker in line:
                end_index = i
                break
        
        # 准备新的Github hosts内容
        new_github_hosts = [start_marker + '\n']
        for domain, ip in github_hosts.items():
            new_github_hosts.append(f"{ip} {domain}\n")
        new_github_hosts.append(end_marker + '\n')
        
        # 构建新的hosts内容
        if start_index != -1 and end_index != -1:
            new_lines = local_lines[:start_index] + new_github_hosts + local_lines[end_index+1:]
        elif start_index != -1:
            new_lines = local_lines[:start_index] + new_github_hosts
        else:
            new_lines = local_lines + ['\n'] + new_github_hosts
        
        return new_lines

    def write_local_hosts(self, lines):
        if os.name == 'nt':
            hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        else:
            hosts_path = "/etc/hosts"
        
        try:
            with open(hosts_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            self.log_signal.emit("hosts文件更新成功！")
            return True
        except PermissionError:
            self.log_signal.emit("权限不足，无法写入hosts文件。请以管理员身份运行程序。")
            return False
        except Exception as e:
            self.log_signal.emit(f"写入hosts文件失败: {e}")
            return False

class FastGithubGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_thread = None

    def init_ui(self):
        # 窗口设置
        self.setWindowTitle("FastGithub")
        # 添加窗口图标（关键修改）
        self.setWindowIcon(QIcon("app.ico"))  # 使用当前目录下的app.ico作为图标
        self.setFixedSize(600, 450)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QLabel#titleLabel {
                font-size: 20px;
                font-weight: bold;
                color: #333333;
            }
            QLabel#statusLabel {
                font-size: 14px;
                color: #666666;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 5px;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
            QFrame {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
        """)

        # 主框架（以下内容保持不变）
        main_frame = QFrame(self)
        self.setCentralWidget(main_frame)
        main_layout = QVBoxLayout(main_frame)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 标题区域
        title_label = QLabel("FastGithub", self)
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 状态区域
        status_layout = QHBoxLayout()
        status_label = QLabel("当前状态: ", self)
        status_label.setObjectName("statusLabel")
        self.status_value = QLabel("未启动", self)
        self.status_value.setObjectName("statusLabel")
        self.status_value.setStyleSheet("color: #ff0000; font-weight: bold;")
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_value)
        status_layout.addStretch(1)
        main_layout.addLayout(status_layout)

        # 按钮区域
        btn_layout = QHBoxLayout()
        self.update_btn = QPushButton("更新 Hosts", self)
        self.update_btn.clicked.connect(self.start_update)
        self.reset_btn = QPushButton("恢复默认", self)
        self.reset_btn.clicked.connect(self.reset_hosts)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.reset_btn)
        main_layout.addLayout(btn_layout)

        # 日志区域
        log_label = QLabel("操作日志:", self)
        log_label.setObjectName("statusLabel")
        main_layout.addWidget(log_label)

        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.NoWrap)
        main_layout.addWidget(self.log_text)

        # 底部信息
        footer_label = QLabel("提示: 请以管理员身份运行以确保功能正常", self)
        footer_label.setObjectName("statusLabel")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #888888; font-size: 12px;")
        main_layout.addWidget(footer_label)

    def start_update(self):
        """开始更新hosts"""
        self.update_btn.setEnabled(False)
        self.reset_btn.setEnabled(False)
        self.status_value.setText("正在更新...")
        self.status_value.setStyleSheet("color: #ff9800; font-weight: bold;")
        
        self.update_thread = UpdateThread()
        self.update_thread.log_signal.connect(self.add_log)
        self.update_thread.result_signal.connect(self.update_finished)
        self.update_thread.start()

    def add_log(self, message):
        """添加日志信息"""
        time_str = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.log_text.append(f"[{time_str}] {message}")
        # 滚动到底部
        self.log_text.moveCursor(self.log_text.textCursor().End)

    def update_finished(self, success):
        """更新完成回调"""
        self.update_btn.setEnabled(True)
        self.reset_btn.setEnabled(True)
        
        if success:
            self.status_value.setText("更新成功")
            self.status_value.setStyleSheet("color: #4CAF50; font-weight: bold;")
            QMessageBox.information(self, "成功", "Github hosts更新完成！\n建议刷新网络或重启浏览器后使用。")
        else:
            self.status_value.setText("更新失败")
            self.status_value.setStyleSheet("color: #ff0000; font-weight: bold;")
            QMessageBox.critical(self, "失败", "Github hosts更新失败！\n请查看日志了解详情。")

    def reset_hosts(self):
        """恢复默认hosts（移除Github相关条目）"""
        reply = QMessageBox.question(self, "确认", "确定要恢复默认hosts吗？\n这将移除所有Github相关条目。",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        try:
            # 读取本地hosts
            local_lines = self.read_local_hosts()
            if local_lines is None:
                QMessageBox.critical(self, "失败", "无法读取hosts文件！")
                return

            # 查找标记并移除相关内容
            start_marker = "# GitHub Hosts Start"
            end_marker = "# GitHub Hosts End"
            
            start_index = -1
            end_index = -1
            
            for i, line in enumerate(local_lines):
                if start_marker in line:
                    start_index = i
                elif end_marker in line:
                    end_index = i
                    break

            # 构建新的hosts内容（移除Github部分）
            if start_index != -1 and end_index != -1:
                new_lines = local_lines[:start_index] + local_lines[end_index+1:]
                # 写入更新后的内容
                if self.write_local_hosts(new_lines):
                    self.add_log("已恢复默认hosts文件")
                    self.status_value.setText("已恢复默认")
                    self.status_value.setStyleSheet("color: #2196F3; font-weight: bold;")
                    QMessageBox.information(self, "成功", "已成功恢复默认hosts文件！")
                else:
                    QMessageBox.critical(self, "失败", "恢复默认hosts失败！")
            else:
                QMessageBox.information(self, "提示", "未找到Github相关条目，无需恢复。")

        except Exception as e:
            self.add_log(f"恢复默认失败: {str(e)}")
            QMessageBox.critical(self, "失败", f"恢复默认hosts失败: {str(e)}")

    # 复用原有的读取和写入方法
    def read_local_hosts(self):
        if os.name == 'nt':
            hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        else:
            hosts_path = "/etc/hosts"
        
        try:
            with open(hosts_path, 'r', encoding='utf-8') as f:
                return f.readlines()
        except PermissionError:
            self.add_log("权限不足，无法读取hosts文件。请以管理员身份运行程序。")
            return None
        except Exception as e:
            self.add_log(f"读取hosts文件失败: {e}")
            return None

    def write_local_hosts(self, lines):
        if os.name == 'nt':
            hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        else:
            hosts_path = "/etc/hosts"
        
        try:
            with open(hosts_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True
        except PermissionError:
            self.add_log("权限不足，无法写入hosts文件。请以管理员身份运行程序。")
            return False
        except Exception as e:
            self.add_log(f"写入hosts文件失败: {e}")
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FastGithubGUI()
    window.show()
    sys.exit(app.exec_())