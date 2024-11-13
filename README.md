# 个人代码使用  
***
## 1.重命名文件.py 使用
### 作用: 批量重命名图片名称
安装打包exe文件库
```
pip install pyinstaller
```
打包重命名文件.py并使用ico图标
```
pyinstaller -F -i pic.ico 重命名文件.py
```

***

## 2.转ICO图片.py 使用说明
能够拖动文件夹批量转换图片为ICO图标，并可以递归实现批量转换

可以对单个图片文件转换为ICO图标

按照判别文件类别轻量库，API文档：https://h2non.github.io/filetype.py/
```
pip install filetype
```

