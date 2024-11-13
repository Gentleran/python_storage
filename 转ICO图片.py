import argparse
import filetype
from pathlib import Path
from PIL import Image
import logging

"""
分类输入路径下的文件(文件夹，图片，其他)，并分类存放
"""


def sort_files(input_path: Path) -> tuple:
    # 初始化三个分类的列表
    folders = []  # 存放文件夹
    images = []  # 存放图片
    other_files = []  # 存放其他文件

    # 得到输入路径下所有文件（不递归）
    files = input_path.glob('*')  # 获取当前目录下的文件和文件夹
    for file in files:
        if file.is_dir():  # 判断是否是文件夹
            folders.append(file)
        else:
            # 判断是否是图片文件
            kind = filetype.guess(file)
            if kind is not None and kind.mime.startswith("image"):
                images.append(file)
            else:
                other_files.append(file)
    return folders, images, other_files


"""
将图片转换为ico格式
"""


def convert_to_ico(input_path, output_path, size):
    with Image.open(input_path) as img:
        img = img.convert('RGBA')
        img.save(output_path, format="ICO", sizes=size)
    return img


def transform_image(input_path, output_path, ico_size, recursive):
    folders, images, other_files = sort_files(input_path)
    # 遍历其他文件
    for other_file in other_files:
        logging.warning(f"文件 {other_file} 不是图片，跳过。")
    # 遍历图片
    for image in images:
        save_path = output_path / image.with_suffix(".ico").name
        logging.info(f"开始转换图片: {image} 到 {save_path} ")
        if not save_path.parent.exists():
            save_path.parent.mkdir(parents=True)  # 当保存路径不存在时创建
        convert_to_ico(image, save_path, ico_size)

    if recursive:
        for folder in folders:
            save_path = output_path / folder.name
            logging.info(f"开始递归转换文件夹: {folder} 到 {save_path} ")
            transform_image(folder, save_path, ico_size, recursive)


if __name__ == '__main__':
    # 设置日志记录
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # 命令行参数解析
    paser = argparse.ArgumentParser(description='将图片转换为ico格式')
    paser.add_argument('input_path', type=str, help='输入图片路径或者文件夹路径')
    paser.add_argument('-o', '--output', type=str, help='输出文件路径')
    paser.add_argument('-s', '--size', type=int, default=256, choices=[16, 32, 48, 64, 128, 256],
                       help='ico图片大小默认:256*256')
    # 是否递归转换默认否
    paser.add_argument("-r", '--recursive', action='store_true', help='是否递归转换图片')
    args = paser.parse_args()

    # 参数解析
    input_path = Path(args.input_path)  # 输入路径
    ico_size = [(args.size, args.size)]  # ico图片大小
    recursive = args.recursive

    if args.output is None:  # 判断输出路径是否为空
        output_path = input_path
    else:
        output_path = Path(args.output)

    if input_path.is_dir():  # 判断输入路径是否为文件夹
        is_image_path = False
        output_path = output_path.with_name(f"{input_path.name}_ico")
    else:
        is_image_path = True
        output_path = output_path.with_suffix('.ico')

    if is_image_path:
        logging.info(f"开始转换图片: {input_path} 到 {output_path}")
        convert_to_ico(input_path, output_path, ico_size)
    else:
        transform_image(input_path, output_path, ico_size, recursive)

    logging.info("程序执行完毕，按任意键退出...")
    input()
