import os
from pathlib import Path
import json
from nonebot.permission import SUPERUSER
from nonebot import require
from nonebot.plugin import PluginMetadata
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin.on import on_message, on_keyword
from nonebot.rule import to_me
from .config import Config
from nonebot import on_command
import httpx  # 替换 requests 用的 httpx
import tomllib
import tomli_w
require("nonebot_plugin_limiter")
require("nonebot_plugin_saa")
require("nonebot_plugin_localstore")

from nonebot_plugin_saa import Image, MessageFactory,Text
from nonebot_plugin_limiter import UserScope, Cooldown
import nonebot_plugin_localstore as store

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-simple-setu",
    description="一个简单到不能再简单的色图插件",
    usage="通过指令获取setu",
    type="application",
    homepage="https://github.com/nomdn/nonebot-plugin-simple-setu",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

config_file = store.get_plugin_config_file("config.toml")
if not config_file.exists():
    config = {
        "simple_setu": {
            "pixiv_proxy": "",
            "enable_setu": True,
            "enable_dress_api_keyword": True,
            "dress_api_url": "",
            "cooldown_time": 0,
            "limit": 10
        }
    }
    with open(config_file, "wb") as f:
        tomli_w.dump(config, f)
with open(config_file, "rb") as f:
    config = tomllib.load(f)
proxy = config["simple_setu"]["pixiv_proxy"]
enable_setu = config["simple_setu"]["enable_setu"]
enable_leg_keyword = config["simple_setu"]["enable_dress_api_keyword"]
dress_api_url = config["simple_setu"]["dress_api_url"]
cooldown_time = config["simple_setu"]["cooldown_time"]
limit = config["simple_setu"]["limit"]

# 创建一个异步客户端


async def get_setu_json(tag: list = None):

    url = f"https://api.lolicon.app/setu/v2"
    if tag:
        if len(tag) > 3:
            raise RuntimeError("标签数量不能超过3个")
    use_proxy = proxy or "pixiv-proxy.wsmdn.dpdns.org"


    async with httpx.AsyncClient() as http_client:
        response = await http_client.post(url,json={
        "r18": 0,
        "tag": tag,
        "proxy": use_proxy})

    return response.json()
async def get_dress_api_data(url: str):
    urls = ["https://api.wsmdn.top/v2/dress","https://dress.wsmdn.top/v1/dress"]

    if not url:
        for url in urls:
            async with httpx.AsyncClient() as http_client:
                try:
                    response = await http_client.get(url)
                    if response.status_code == 200:
                        response = response.json()
                except httpx.RequestError:
                    continue
        else:
            raise RuntimeError("所有API请求失败")
    else:
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(url)
            if response.status_code == 200:
                response = response.json()
            raise RuntimeError("API请求失败")
    finally_result = {
        "author": "",
        "hash": "",
        "time": "",
        "path": "",
        
    }
    try:
    
        url = response["img_url"]
        update_time = response["upload_time"]
        author = response["img_author"]
    except:
        url = response["path"]
        update_time = response["time"]
        author = response["author"]
    finally_result["author"] = author
    finally_result["hash"] = response["hash"]
    finally_result["time"] = update_time
    finally_result["path"] = url
    return finally_result
setu = on_command("setu", aliases={"色图", "来份色图"})
@setu.handle(parameterless=[
    Cooldown(
        UserScope(  # entity, `UserScope` 统计范围为所有用户在任意场景的使用量
        permission=SUPERUSER
        ),    # 两种白名单方式
        int(cooldown_time),    # period, 冷却时长，单位为秒
        limit = limit,  # 最大触发次数
        reject = "要被玩爆了喵", # 可选，超额使用时的提示词
        name = "simple-setu" # 可选，使用统计集合名称，填写名称将开启该集合的持久化
    )])
async def handle_function(
    args: Message = CommandArg(),
):
    if enable_setu:
        if tags := args.extract_plain_text():
            tags = tags.split(" ")[:3]
        for i in range(5):
            try:  
                data = await get_setu_json(tag=tags)
                if data["data"]:
                    break
                else:
                    await setu.finish("没有找到结果喵~")
            except Exception as e:
                error =e
                continue

        else:
            await setu.finish(f"请求色图API失败了喵~,{error}")
        data = data["data"][0]
        pid = data["pid"]
        title = data["title"]
        author = data["author"]
        image_url = data["urls"]["original"]
        MessageText = Text(f"\n作品PID:{pid}\n标题:{title}\n作者:{author}\n")
        MessageImage = Image(image_url)
        await MessageFactory([MessageText,MessageImage]).send(at_sender=True,
                                                            reply=True)
    else:
        await setu.finish("主人想让你戒色喵~")
femboy = on_command("dress-api", aliases={"小南梁", "小男娘"})
@femboy.handle(parameterless=[
    Cooldown(
        UserScope(  # entity, `UserScope` 统计范围为所有用户在任意场景的使用量
        permission=SUPERUSER
        ),    # 两种白名单方式
        int(cooldown_time),    # period, 冷却时长，单位为秒
        limit = limit,  # 最大触发次数
        reject = "要被玩爆了喵", # 可选，超额使用时的提示词
        name = "simple-dress-api" # 可选，使用统计集合名称，填写名称将开启该集合的持久化
    )])
async def handle_femboy(
):
    if enable_leg_keyword:
        for i in range(5):
            try:
                if dress_api_url:
                    data = await get_dress_api_data(url=dress_api_url)
                else: 
                    data = await get_dress_api_data(url=None)
                break
            except RuntimeError as e:
                continue
                error = e
            except Exception as e:
                error = e
                continue
        else:
          await femboy.finish(f"请求API失败了喵~,{error}")
        url = data["path"]
        update_time = data["time"]
        author = data["author"]
        MessageText = Text(f"\n上传时间:{update_time}\n贡献者:{author}\nNotice:Cute-Dress/Dress CC BY-NC-SA 4.0\n")
        MessageImage = Image(url)
        await MessageFactory([MessageText,MessageImage]).send(at_sender=True,
                                                            reply=True)
        await femboy.finish()
    else:
        await femboy.finish("主人不想让你看小男娘喵")


