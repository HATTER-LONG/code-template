# pyside6-fluent-widgets-template

## 依赖

- [Pyside6](https://wiki.qt.io/Qt_for_Python)：UI 依赖；
- [PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)：UI 依赖；
- [pebble](https://github.com/noxdafox/pebble)：多线程/进程管理；
- [pyinstaller](https://pyinstaller.org/en/stable/)：打包依赖；

## 使用方法

### 基础配置

1. 创建虚拟环境:
   - conda: `conda create -n [env_name] python=3.11;conda activate [env_name]`
   - venv: `python3 -m venv ./[env_name]; source ./[env_name]/bin/activate`
2. 安装 poetry：`pip install -U pip setuptools;pip install poetry`
3. 安装项目依赖：`poetry install`

### 需要修改

1. [pyproject.toml](./pyproject.toml) 中的项目信息；
2. `poetry update;poetry lock` 更新依赖库；
3. 修改 README；

### poetry 基本使用

1. 基本使用：

   - 创建项目：`poetry new [project_name]`
   - 已有项目：`poetry init`
   - 安装依赖：`poetry install`
   - 添加依赖：`poetry add [package]`
   - 移除依赖：`poetry remove [package]`
   - 更新依赖：`poetry update`
     - 更新指定依赖：`poetry add [packeage]@[version|latest]`

2. 使用 poetry 的虚拟环境：

   - 查看当前环境：`poetry env info`
   - 切换 python 版本: `pyenv local [version]; poetry env use [python-path]`
   - 进入 poetry 虚拟环境 shell：`poetry shell`
   - 退出 poetry 虚拟环境，注意直接 deactivate 是不行的：`exit`
