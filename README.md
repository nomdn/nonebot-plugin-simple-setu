<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://cdn.jsdelivr.net/gh/nomdn/nonebot-plugin-simple-setu@resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://cdn.jsdelivr.net/gh/nomdn/nonebot-plugin-simple-setu@resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-simple-setu

_✨ NoneBot 简单色图插件 ✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/badge/License-LGPL%20v3.0-green.svg" alt="license">
</a>
<a href="https://pypi.org/project/nonebot-plugin-simple-setu/">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-simple-setu.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 介绍
一个简单到不能再简单的色图插件
正在进行大重构

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-simple-setu

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-simple-setu
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-simple-setu
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-simple-setu
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-simple-setu
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_simple_setu"]

</details>

## ⚙️ 配置

在 系统配置目录 nonebot2/nonebot_plugin_simple_setu/config.toml 中修改以下内容
```` toml
[simple_setu]
# pixiv 图片proxy（可选）
pixiv_proxy = ""
# 功能开关
enable_setu = true
enable_dress_api_keyword = true
# dress-api url配置（可选）
dress_api_url = ""
# 冷却时间
cooldown_time = 10
# 速率限制
limit= 2

````

## 🎉 使用
### 指令表
|  指令   |  权限  | 需要@ | 范围 | 说明 |
|:-----:|:----:|:---:|:--:|:----:|
| /setu |  群员  |  否  | 群聊 | 随机获得一张色图,后面可以加tag，如/setu tag |
| /dress-api  |  群员  |  否  | 群聊 | 获取一张男娘图片 |
### 效果图



