import os
from tkinter import Tk, Label, Button, filedialog, messagebox
from PIL import Image, PngImagePlugin

def split_prompt(prompt, max_length=148):
    # 初始化结果列表和当前段落
    result = []
    current_segment = ""

    # 按逗号分隔字符串
    words = prompt.split(',')

    for word in words:
        # 保持符号和空格
        word = word.strip() + ','  # 确保每个词后面都有逗号
        
        # 检查当前段落加上新词是否超过最大长度
        if len(current_segment) + len(word) > max_length:
            # 如果超过，先将当前段落添加到结果中
            result.append(current_segment.strip())  # 去掉末尾多余空格
            # 重置当前段落为新词
            current_segment = word
        else:
            # 如果没有超过，添加新词到当前段落
            current_segment += ' ' + word if current_segment else word

    # 添加最后一个段落
    if current_segment:
        result.append(current_segment.strip())

    # 将结果列表中的段落用换行符连接
    return '\n'.join(result)

def remove_last_character(s):
    return s[:-1]  # 使用切片去掉最后一个字符

def write_prompt(data):
    p = split_prompt(data)
    p = remove_last_character(p)
    return p

def read_txt_file(file_path):
    """从文本文件中按行读取内容并返回格式修改后的字符串列表"""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 使用 write_prompt 函数对每行字符串进行格式修改
    return [write_prompt(line.strip()) for line in lines]  # 去除每行的前后空白字符并格式化

def create_png_images(output_folder, num_images):
    """在目标文件夹内生成指定数量的空白 PNG 图片"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # 创建目标文件夹

    for i in range(num_images):
        img = Image.new('RGB', (100, 100), color='white')  # 创建 100x100 的白色图像
        img_path = os.path.join(output_folder, f'{(i + 1):04d}.png')
        img.save(img_path)  # 保存 PNG 图片

def write_hidden_info_to_png(image_path, info):
    # 打开图像
    image = Image.open(image_path)

    # 创建 PNG 信息对象
    png_info = PngImagePlugin.PngInfo()

    png_info.add_text("parameters", info)

    # 保存图像并附加 PNG 信息
    image.save(image_path, pnginfo=png_info)

def process_file(txt_file_path, output_folder):
    # 读取文本文件内容并格式化
    lines = read_txt_file(txt_file_path)

    # 生成对应数量的 PNG 图片
    create_png_images(output_folder, len(lines))

    # 将每行字符串写入对应的 PNG 图片的隐藏信息
    for i, line in enumerate(lines):
        image_path = os.path.join(output_folder, f'{(i + 1):04d}.png')
        write_hidden_info_to_png(image_path, line)

    messagebox.showinfo("成功", "PNG 图片已生成并写入隐藏信息！")

def select_txt_file():
    """选择文本文件并处理"""
    txt_file_path = filedialog.askopenfilename(title="选择 TXT 文件", filetypes=[("Text Files", "*.txt")])
    if txt_file_path:
        output_folder = filedialog.askdirectory(title="选择输出文件夹")
        if output_folder:
            process_file(txt_file_path, output_folder)

# 创建主窗口
root = Tk()
root.title("TXT 转 PNG 生成器")
root.geometry("300x200")

# 添加标签和按钮
label = Label(root, text="选择一个 TXT 文件生成对应的 PNG 图片")
label.pack(pady=20)

button = Button(root, text="选择 TXT 文件", command=select_txt_file)
button.pack(pady=10)

# 启动 GUI 主循环
root.mainloop()
