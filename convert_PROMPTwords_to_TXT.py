import os

# 定义文件夹路径
folder_path = r'E:\MyResource\JustForFun\005loraOUT\data\001matureMM\r004'  # 替换为您的文件夹路径
output_file_path = r'E:\MyResource\JustForFun\005loraOUT\data\001matureMM\out_r004.txt'  # 输出文件路径

forename ='best quality,highly detailed,masterpiece,ultra-detailed,illustration,1girl,short hair,blue eyes,bangs,skin fang,grey hair,fang,hair between eyes'
# forename = '"' + forename

behindname = '<lora:nwsj_flux:1>,'
# behindname = behindname + '"'

# 获取文件夹内所有 txt 文件，并按名称排序
txt_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')])

# 打开输出文件
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        with open(file_path, 'r', encoding='utf-8') as input_file:
            for line in input_file:
                # 去掉行末的换行符，并添加前后文字
                # modified_line = f"--prompt {forename},{line.strip()},{behindname}\n"
                modified_line = f"{forename},{line.strip()},{behindname}\n"
                # modified_line = f"{line.strip()}\n"
                output_file.write(modified_line)

print(f"所有内容已写入到 {output_file_path}")
