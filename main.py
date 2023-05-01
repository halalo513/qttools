from DatasetSplit import SplitDataset
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox,QDesktopWidget


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建界面元素
        self.dataset = None
        self.input_folder_label = QLabel("根目录：", self)
        self.input_folder_label.move(20, 20)
        self.input_folder_edit = QLineEdit(self)
        self.input_folder_edit.move(120, 20)
        self.input_folder_edit.setReadOnly(True)
        self.input_folder_button = QPushButton("打开", self)
        self.input_folder_button.move(400, 20)
        self.input_folder_button.clicked.connect(self.open_input_folder)

        self.output_folder_label = QLabel("输出目录：", self)
        self.output_folder_label.move(20, 60)
        self.output_folder_edit = QLineEdit(self)
        self.output_folder_edit.move(120, 60)
        self.output_folder_edit.setReadOnly(True)
        self.output_folder_button = QPushButton("选择", self)
        self.output_folder_button.move(400, 60)
        self.output_folder_button.clicked.connect(self.open_output_folder)

        self.input3_label = QLabel("训练集比例：", self)
        self.input3_label.move(20, 100)
        self.input3_edit = QLineEdit(self)
        self.input3_edit.move(120, 100)

        self.input4_label = QLabel("验证集比例：", self)
        self.input4_label.move(20, 140)
        self.input4_edit = QLineEdit(self)
        self.input4_edit.move(120, 140)

        self.input5_label = QLabel("测试集比例：", self)
        self.input5_label.move(20, 180)
        self.input5_edit = QLineEdit(self)
        self.input5_edit.move(120, 180)

        self.input6_label = QLabel("随机数种子：", self)
        self.input6_label.move(20, 220)
        self.input6_edit = QLineEdit(self)
        self.input6_edit.move(120, 220)

        self.submit_button = QPushButton("开始划分", self)
        self.submit_button.move(200, 300)
        self.submit_button.clicked.connect(self.submit)

        # 初始化界面
        # 获取屏幕的宽度和高度
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()

        # 计算窗口的位置，使其在屏幕中心
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.setGeometry(x, y, 500, 360)
        self.setWindowTitle("Yolo数据集划分")
        self.setFixedSize(500, 360)
        self.show()

        # 初始化变量
        self.input_folder = ""
        self.output_folder = ""

    def open_input_folder(self):
        # 打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(self, "选择根目录")
        if folder_path:
            self.input_folder = folder_path
            self.input_folder_edit.setText(folder_path)

    def open_output_folder(self):
        # 打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if folder_path:
            self.output_folder = folder_path
            self.output_folder_edit.setText(folder_path)

    def submit(self):
        # 校验输入
        input3 = self.input3_edit.text()
        input4 = self.input4_edit.text()
        input5 = self.input5_edit.text()
        input6 = self.input6_edit.text()

        if not self.input_folder:
            QMessageBox.warning(self, "警告", "请选择根目录！")
            return

        if not self.output_folder:
            QMessageBox.warning(self, "警告", "请选择输出目录！")
            return
        try:
            input3 = float(input3)
            input4 = float(input4)
            input5 = float(input5)
            input6 = int(input6)
        except ValueError:
            QMessageBox.warning(self, "警告", "输入必须是数字！")
            return

        if input3 < 0 or input3 > 1:
            QMessageBox.warning(self, "警告", "训练集比例必须在0和1之间！")
            return

        if input4 < 0 or input4 > 1:
            QMessageBox.warning(self, "警告", "验证集比例必须在0和1之间！")
            return

        if input5 < 0 or input5 > 1:
            QMessageBox.warning(self, "警告", "测试集比例必须在0和1之间！")
            return

        if input3 + input4 + input5 != 1.00:
            QMessageBox.warning(self, "警告", "训练集、验证集和测试集的比例总和必须为1！")
            return

        if input6 < 1 or input6 > 100:
            QMessageBox.warning(self, "警告", "输入6必须在1和100之间！")
            return
        try:
            self.dataset = SplitDataset(inputDir=self.input_folder, outputDir=self.output_folder,
                                   percents=[input3, input4, input5],seed=input6
                                   )
            self.dataset.result_ready.connect(self.worker_finished)
            self.dataset.start()
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "错误", "划分失败")

    def worker_finished(self, data_dict):
        # 更新状态标签，并显示结果
        success_info = f"训练集:{data_dict.get('train_num')};验证集:{data_dict.get('val_num')};测试集:{data_dict.get('test_num')}"
        QMessageBox.information(self, "提示", success_info)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyWindow()
    main_window.show()
    sys.exit(app.exec_())
    # dataset = SplitDataset(inputDir=r'C:\Users\XiaoS\Desktop\桌面\boat')
    # print(dataset.split())