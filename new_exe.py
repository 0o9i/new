# 导入所需的库
import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from PIL import Image, ImageTk

# 创建一个主窗口
window = tk.Tk()
window.title("图像分类汇总程序")
window.geometry("800x600")

# 创建一个标签显示标题
label_title = tk.Label(window, text="图像分类汇总程序", font=("Arial", 24))
label_title.pack()

# 创建一个标签显示说明
label_instruction = tk.Label(window, text="请选择一个包含图片的文件夹，然后输入要查询的日期范围（格式为YYYY-MM-DD），\n点击查询按钮查看结果", font=("Arial", 16))
label_instruction.pack()


# 创建一个按钮选择文件夹
def select_folder():
    global folder_path  # 定义一个全局变量存储文件夹路径
    folder_path = filedialog.askdirectory()  # 弹出对话框选择文件夹
    label_folder.config(text="已选择文件夹：" + folder_path)  # 更新标签显示文件夹路径


button_folder = tk.Button(window, text="选择文件夹", font=("Arial", 16), command=select_folder)
button_folder.pack()

# 创建一个标签显示文件夹路径
label_folder = tk.Label(window, text="未选择文件夹", font=("Arial", 16))
label_folder.pack()

# 创建两个输入框输入日期范围
label_start = tk.Label(window, text="开始日期：", font=("Arial", 16))
label_start.pack()
entry_start = tk.Entry(window, font=("Arial", 16))
entry_start.pack()
label_end = tk.Label(window, text="结束日期：", font=("Arial", 16))
label_end.pack()
entry_end = tk.Entry(window, font=("Arial", 16))
entry_end.pack()


# 创建一个按钮查询结果
def query_result():
    global df  # 定义一个全局变量存储数据框
    df = pd.DataFrame(columns=["日期", "图片路径", "类别"])  # 创建一个空的数据框，有三列：日期，图片路径，类别
    for file in os.listdir(folder_path):  # 遍历文件夹中的每个文件
        if file.endswith(".jpg") or file.endswith(".png"):  # 如果是图片文件
            date = file.split("_")[0]  # 提取图片文件名中的日期部分，假设图片文件名的格式为YYYY-MM-DD_XXXX.jpg或者.png
            path = os.path.join(folder_path, file)  # 拼接图片文件的完整路径
            category = file.split("_")[-1].split(".")[0] # 提取图片文件名中的类别部分，即ok或者ng
            df = pd.concat([df, pd.DataFrame({"日期": [date], "图片路径": [path], "类别": [category]})], ignore_index=True)  # 将这一行数据添加到数据框中

    start_date = entry_start.get()  # 获取输入框中的开始日期
    end_date = entry_end.get()  # 获取输入框中的结束日期
    df = df[(df["日期"] >= start_date) & (df["日期"] <= end_date)]  # 筛选出在日期范围内的数据

    summary_df = df.groupby("日期")["类别"].value_counts(normalize=True).unstack().fillna(
        0)  # 对数据框按照日期和类别进行分组统计，计算每个日期每个类别的占比，并转换成宽表形式，缺失值填充为0
    summary_df["ok"] = summary_df["ok"].apply(lambda x: "{:.2%}".format(x))  # 将ok列的数值转换成百分比格式，保留两位小数
    summary_df["ng"] = summary_df["ng"].apply(lambda x: "{:.2%}".format(x))  # 将ng列的数值转换成百分比格式，保留两位小数

    label_result.config(text="查询结果如下：")  # 更新标签显示查询结果

    for widget in frame_result.winfo_children():  # 清空结果框架中的所有组件
        widget.destroy()

    for i in range(len(summary_df)):  # 遍历每一行数据
        date = summary_df.index[i]  # 获取日期
        ok_ratio = summary_df.iloc[i]["ok"]  # 获取ok占比
        ng_ratio = summary_df.iloc[i]["ng"]  # 获取ng占比

        label_date = tk.Label(frame_result, text=date, font=("Arial", 16))  # 创建一个标签显示日期
        label_date.grid(row=i, column=0)  # 将标签放在结果框架中的第i行第0列

        label_ok_ratio = tk.Label(frame_result, text=ok_ratio, font=("Arial", 16))  # 创建一个标签显示ok占比
        label_ok_ratio.grid(row=i, column=1)  # 将标签放在结果框架中的第i行第1列

        label_ng_ratio = tk.Label(frame_result, text=ng_ratio, font=("Arial", 16))  # 创建一个标签显示ng占比
        label_ng_ratio.grid(row=i, column=2)  # 将标签放在结果框架中的第i行第2列

        def show_images(date):  # 定义一个函数显示某个日期内的所有图片
            sub_df = df[df["日期"] == date]  # 筛选出该日期对应的数据子集

            for widget in frame_images.winfo_children():  # 清空图片框架中的所有组件
                widget.destroy()

            for j in range(len(sub_df)):  # 遍历每一行数据子集
                path = sub_df.iloc[j]["图片路径"]  # 获取图片路径

                image = Image.open(path)  # 打开图片文件
                image.thumbnail((100, 100))  # 缩放图片大小为100x100像素

                photo = ImageTk.PhotoImage(image)  # 将图片转换成tkinter可用的格式

                label_image = tk.Label(frame_images, image=photo)  # 创建一个标签显示图片
                label_image.image = photo  # 防止图片被垃圾回收机制回收

                label_image.grid(row=j // 5, column=j % 5)  # 将标签放在图片框架中的第j//5行第j%5列（每行最多显示5张图片）

        button_view = tk.Button(frame_result, text="查看", font=("Arial", 16),
                                command=lambda: show_images(date))  # 创建一个按钮查看该日期内的所有图片，点击时调用show_images函数，并传入当前日期作为参数
        button_view.grid(row=i, column=3)  # 将按钮放在结果框架中的第i行第3列


button_query = tk.Button(window, text="查询", font=("Arial", 16), command=query_result)
button_query.pack()

# 创建一个标签显示查询结果标题
label_result = tk.Label(window, text="查询结果", font=("Arial", 16))
label_result.pack()

# 创建一个框架显示查询结果表格（包括查看按钮）
frame_result = tk.Frame(window)
frame_result.pack()

# 创建一个框架显示查询结果对应的所有图片（按照查看按钮选择）
frame_images = tk.Frame(window)
frame_images.pack()

# 使用PyInstaller将这个.py文件打包成.exe文件，命令如下：
# pyinstaller -F -w -i icon.ico image_summary.py

window.mainloop()  # 进入主循环