import os
import re
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, \
    QFileDialog,QVBoxLayout
from PyQt5.QtGui import QPixmap



# 定义一个函数，根据文件名获取图片的日期和类别
def get_date_and_category(filename):
    # 使用正则表达式匹配文件名中的日期和类别
    pattern = r"(\d{4}-\d{2}-\d{2}-\d{4})_(ok|ng)\.jpg"
    match = re.search(pattern, filename)
    if match:
        # 如果匹配成功，返回日期和类别
        date = match.group(1)
        category = match.group(2)
        return date, category
    else:
        # 如果匹配失败，返回None
        return None


# 定义一个函数，根据给定的日期范围和文件夹路径，统计图片的数量和百分比
def summarize_images(start_date, end_date, folder):
    # 创建一个空字典，用于存储每个日期的图片数量和百分比
    summary = {}
    # 获取文件夹下的所有文件名
    files = os.listdir(folder)
    # 遍历每个文件名
    for file in files:
        # 获取文件名对应的日期和类别
        date, category = get_date_and_category(file)
        # 如果日期和类别都不为空，并且日期在给定的范围内
        if date and category and start_date <= date <= end_date:
            # 如果日期不在字典中，创建一个新的键值对，初始值为[0, 0]
            if date not in summary:
                summary[date] = [0, 0]
            # 如果类别是ok，将字典中对应的列表的第一个元素加一
            if category == "ok":
                summary[date][0] += 1
            # 如果类别是ng，将字典中对应的列表的第二个元素加一
            if category == "ng":
                summary[date][1] += 1
    # 遍历字典中的每个键值对
    for date, counts in summary.items():
        # 计算总数和百分比，并将列表更新为[ok数, ng数, ok百分比, ng百分比]
        total = sum(counts)
        ok_percentage = round(counts[0] / total * 100, 2)
        ng_percentage = round(counts[1] / total * 100, 2)
        summary[date] = [counts[0], counts[1], ok_percentage, ng_percentage]
    # 返回字典
    return summary


# 定义一个函数，根据给定的日期范围和文件夹路径，显示图片的表格信息和查看按钮
def show_images(start_date, end_date, folder):
    # 调用上面定义的函数，获取图片的统计信息
    summary = summarize_images(start_date, end_date, folder)
    # 创建一个表格控件，设置行数为字典的长度，列数为4
    table = QTableWidget(len(summary), 4)
    # 设置表格的标题为["时间", "ok百分比", "ng百分比", "查看"]
    table.setHorizontalHeaderLabels(["时间", "ok百分比", "ng百分比", "查看"])
    # 设置表格的行高为30像素，列宽为100像素
    # 设置表格的行高为30像素
    for i in range(len(summary)):
        table.setRowHeight(i, 30)

    # 设置表格的列宽为100像素
    for j in range(4):
        table.setColumnWidth(j, 100)

    # 遍历字典中的每个键值对，按照顺序填充表格中的每一行
    for i, (date, data) in enumerate(summary.items()):
        # 创建一个标签控件，显示日期，并将其添加到表格中第i行第0列
        label = QLabel(date)
        table.setCellWidget(i, 0, label)
        # 创建两个标签控件，显示ok百分比和ng百分比，并将其添加到表格中第i行第1列和第2列
        ok_label = QLabel(str(data[2]) + "%")
        ng_label = QLabel(str(data[3]) + "%")
        table.setCellWidget(i, 1, ok_label)
        table.setCellWidget(i, 2, ng_label)
        # 创建一个按钮控件，显示"查看"，并将其添加到表格中第i行第3列
        button = QPushButton("查看")
        table.setCellWidget(i, 3, button)
        # 给按钮绑定一个点击事件，调用另一个函数来显示该日期下的所有图片，并传入文件夹路径作为参数
        button.clicked.connect(lambda: show_images_by_date(date, folder))
    # 返回表格控件
    return table


# 定义一个函数，根据给定的日期和文件夹路径，显示该日期下的所有图片
# 定义一个全局变量来存储文件对话框对象
dialogs = []

# def show_images_by_date(date, folder):
#     images = []
#     files = os.listdir(folder)
#     for file in files:
#         date_, category = get_date_and_category(file)
#         if date_ and category and date_ == date:
#             images.append(os.path.join(folder, file))
#     dialog = QFileDialog()
#     dialog.setWindowTitle("查看图片")
#     dialog.setNameFilter("Images (*.jpg)")
#     # 设置文件对话框的模式和选项
#     dialog.setFileMode(QFileDialog.ExistingFiles)
#     dialog.setOption(QFileDialog.ReadOnly, True)
#     dialog.setDirectory(folder)
#     dialog.selectFile(images[0])
#     dialog.show()
#     dialogs.append(dialog)
def show_images_by_date(date, folder):
    images = []
    files = os.listdir(folder)
    for file in files:
        date_, category = get_date_and_category(file)
        if date_ and category and date_ == date:
            images.append(os.path.join(folder, file))
    # 创建一个新的窗口
    window = QWidget()
    window.setWindowTitle("查看图片")
    # 创建一个QLabel控件
    label = QLabel()
    # 设置QLabel控件的大小和缩放模式
    label.setFixedSize(800, 600)
    label.setScaledContents(True)
    # 设置QLabel控件的图片为第一张符合的图片
    pixmap = QPixmap(images[0])
    label.setPixmap(pixmap)
    # 将QLabel控件添加到窗口中
    window.setLayout(QVBoxLayout())
    window.layout().addWidget(label)
    # 显示窗口
    window.show()
    dialogs.append(window)

# 创建一个应用程序对象
app = QApplication([])
# 创建一个窗口控件，并设置标题为"图片统计"
window = QWidget()
window.setWindowTitle("图片统计")
# 创建五个标签控件，并设置文本为"选择文件夹", "开始日期", "终止日期", "格式: yyyy-mm-dd-hhmm", "结果"
folder_label = QLabel("选择文件夹")
start_label = QLabel("开始日期")
end_label = QLabel("终止日期")
format_label = QLabel("格式: yyyy-mm-dd-hhmm")
result_label = QLabel("结果")
# 创建两个输入框控件，并设置占位符文本为"请输入开始日期"和"请输入终止日期"
start_edit = QLineEdit()
start_edit.setPlaceholderText("请输入开始日期")
end_edit = QLineEdit()
end_edit.setPlaceholderText("请输入终止日期")
# 创建两个按钮控件，并设置文本为"浏览"和"查询"
browse_button = QPushButton("浏览")
query_button = QPushButton("查询")
# 给浏览按钮绑定一个点击事件，调用另一个函数来选择并显示文件夹路径
browse_button.clicked.connect(lambda: select_folder())
# 给查询按钮绑定一个点击事件，调用另一个函数来获取输入框中的内容并显示结果表格，并传入文件夹路径作为参数
query_button.clicked.connect(lambda: show_result(folder))
# 定义一个变量来存储选择的文件夹路径，默认为空字符串（表示当前目录）
folder = ""


# 定义一个函数来选择并显示文件夹路径
def select_folder():
    global folder
    folder = QFileDialog.getExistingDirectory(window, "选择文件夹", ".")
    folder_label.setText(f"选择文件夹：{folder}")


# 定义一个函数来获取输入框中的内容并显示结果表格，并接收一个参数表示文件夹路径
def show_result(folder):
     start_date= start_edit.text().strip()
     end_date= end_edit.text().strip()
     try:
         # 尝试将输入框中的内容转换为datetime对象，并格式化为字符串形式（yyyy-mm-dd-hhmm）
         start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d-%H%M").strftime("%Y-%m-%d-%H%M")
         end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d-%H%M").strftime("%Y-%m-%d-%H%M")
         # 调用上面定义的函数，根据输入框中的内容和文件夹路径显示结果表格，并将其添加到窗口控件中（替换原来的结果标签）
         table = show_images(start_date, end_date, folder)
         window.layout().replaceWidget(result_label, table)

     except ValueError:
         # 如果转换失败（输入格式不正确），则弹出提示信息，并清空输入框内容
         print("请输入正确格式的日期！")
         start_edit.clear()
         end_edit.clear()

     # 设置窗口的布局为垂直布局，并添加所有的控件
window.setLayout(QVBoxLayout())
window.layout().addWidget(folder_label)
window.layout().addWidget(browse_button)
window.layout().addWidget(start_label)
window.layout().addWidget(start_edit)
window.layout().addWidget(end_label)
window.layout().addWidget(end_edit)
window.layout().addWidget(format_label)
window.layout().addWidget(query_button)
window.layout().addWidget(result_label)
     # 显示窗口控件
window.show()
     # 运行应用程序
app.exec_()
