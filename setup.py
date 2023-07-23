from shutil import rmtree
import pip
import sys
import os

# 版本
name = "langful"
version = "0.40"

# 更新与导入
pip.main( [ "install" , "--upgrade" , "setuptools" , "wheel" , "twine" ] )
import setuptools

# 清除无用目录
if os.path.exists( "build" ) :
    rmtree( "build" )
if os.path.exists( f"{ name }.egg-info" ) :
    rmtree( f"{ name }.egg-info" )
if os.path.exists( "dist" ) :
    rmtree( "dist" )
if os.path.exists( os.path.join( f"{ name }" , "__pycache__" ) ) :
    rmtree( os.path.join( f"{ name }" , "__pycache__" ) )

# 参数
sys.argv = [ "setup.py" , "bdist_wheel" ]

# 读取README.md
with open( "README.md" , "r" , encoding = "utf-8" ) as file :
    long_description = file.read()

# 模块信息
setuptools.setup(
    name = name ,
    version = version ,
    author = "cueavyqwp" ,
    author_email = "cueavyqwp@outlook.com" ,
    description = "Help to localization" ,
    long_description = long_description ,
    long_description_content_type = "text/markdown" ,
    url = "https://github.com/cueavy/langful" ,
    packages = setuptools.find_packages() ,
    classifiers = [
        "Programming Language :: Python :: 3" ,
        "License :: OSI Approved :: MIT License" ,
        "Operating System :: OS Independent" ,
    ] ,
    python_requires = '>= 3.9' ,
)

# 清理
rmtree( "build" )
rmtree( f"{ name }.egg-info" )

# 上传pypi
input( "pass enter to upload\n>" )
os.system( "twine upload dist/*" )

# 在 %USERPROFILE% 创建 .pypirc 文件
# 并写入( 记得删除井号 )

# [distutils]
# index-servers = pypi
#
# [pypi]
# username = 用户名
# password = 密码

# 即可自动登录
