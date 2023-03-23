import setuptools
with open( "README.md" , "r" , encoding = "utf-8" ) as fh :
    long_description = fh.read()
setuptools.setup(
    name="langful" , # 模块名称
    version="0.19" , # 当前版本
    author="cueavyqwp" , # 作者
    author_email="cueavyqwp@outlook.com" , # 作者邮箱
    description="", # 模块简介
    long_description=long_description , # 模块详细介绍
    long_description_content_type="text/markdown" , # 模块详细介绍格式
    url="https://github.com/cueavyqwp/langful" , # 模块github地址
    packages=setuptools.find_packages() , # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3" ,
        "License :: OSI Approved :: MIT License" ,
        "Operating System :: OS Independent" ,
    ],
    # 依赖模块
    install_requires=[
    ],
    python_requires='> 3.6' ,
)
# 删除文件夹 build 和 langful.egg-info
# 检查setuptools更新 python -m pip install --user --upgrade setuptools wheel
# 生成whl文件 python setup.py bdist_wheel --universal
# 安装模块 pip install twine
# 上传whl文件 twine upload dist/*
# 安装模块 pip install langful