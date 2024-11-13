import argparse
import sys
from pathlib import Path
from PIL import Image
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 参数解析
parser = argparse.ArgumentParser(description="转换指定文件夹中的图片为 JPG 格式")
parser.add_argument("input_path", type=str, help="输入文件夹路径")
parser.add_argument("-p", "--name_prefix", type=str, nargs="?", default="", help="输出文件名的前缀")
args = parser.parse_args()

input_path = Path(args.input_path)
name_prefix = args.name_prefix

# 检查输入路径是否有效
if not input_path.is_dir():
    logging.error(f"输入路径 {input_path} 无效或不存在！")
    exit(1)

# 过滤图像文件（例如，PNG、BMP 等）
valid_extensions = {'.png', '.bmp', '.tiff', '.jpeg', '.gif', '.jpg', '.webp'}
image_files = [file for file in input_path.glob("*.*") if file.suffix.lower() in valid_extensions]

updated_files = set()
for idx in range(1, len(image_files)+1):
    updated_files.add(f"{name_prefix}{idx}.jpg")

for image_file in image_files:  # 从1开始编号
    try:
        if image_file.name in updated_files:
            logging.warning(f"文件 {image_file} 已被存在，跳过。")
            continue
        # 打开原始图像
        with Image.open(image_file) as img:
            # 转换为 JPG 格式
            img = img.convert('RGB')
            # 构建新的文件名
            idx = 1
            new_file_name = input_path / f"{name_prefix}{idx}.jpg"  # 强制保存为 .jpg 格式

            while new_file_name.exists():
                idx += 1
                new_file_name = input_path / f"{name_prefix}{idx}.jpg"

            # 删除原始文件
            image_file.unlink()  # 删除原文件
            # 保存为 JPG 格式
            img.save(new_file_name, 'JPEG')

            logging.info(f"成功转换并保存了 {image_file} 为: {new_file_name} ，已删除原文件。")
    except Exception as e:
        logging.error(f"处理文件 {image_file} 时发生错误: {e}")

input("程序执行完毕，按任意键退出...")
