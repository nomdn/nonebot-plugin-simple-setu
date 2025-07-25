from json import JSONDecodeError
from pathlib import Path
import json

import nonebot
from nonebot import get_plugin_config
from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent, ActionFailed
from nonebot.exception import MatcherException
from nonebot.plugin import PluginMetadata
from nonebot.adapters import Message
from nonebot.params import CommandArg
from .config import Config
from nonebot import on_command
import httpx  # 替换 requests 用的 httpx

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-simple-setu",
    description="一个简单到不能再简单的色图插件",
    usage="通过指令获取setu",
    type="application",
    homepage="https://github.com/nomdn/nonebot-plugin-simple-setu",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

config = get_plugin_config(Config)

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)

# 创建一个异步客户端
http_client = httpx.AsyncClient()

setu = on_command("setu", aliases={"色图", "来份色图"})

@setu.handle()
async def handle_function(event: MessageEvent, args: Message = CommandArg()):
    if config.api_url == 0:
        # 提取参数纯文本作为地名，并判断是否有效
        if tag := args.extract_plain_text():
            sender_qq = event.get_user_id()
            # 使用 httpx 替换 requests
            try:
                response = await http_client.get(f"https://api.lolicon.app/setu/v2?tag={tag}")
                json_dict = response.json()
                title = json_dict["data"][0]["title"]
                pid = json_dict["data"][0]["pid"]
                author = json_dict["data"][0]["author"]
                url = json_dict["data"][0]["urls"]["original"]
                await setu.send(MessageSegment.at(sender_qq)+f"\n标题:{title}\nPID:{pid}\n作者:{author}")
                await setu.finish(MessageSegment.image(f"{url}"))
            except MatcherException:
                raise
            except Exception as e:
                await setu.finish(f"发生错误：{e}")
        else:
            try:
                sender_qq = event.get_user_id()
                response = await http_client.get(f"https://api.lolicon.app/setu/v2")
                json_dict = response.json()
                title = json_dict["data"][0]["title"]
                pid = json_dict["data"][0]["pid"]
                author = json_dict["data"][0]["author"]
                url = json_dict["data"][0]["urls"]["original"]
                await setu.send(MessageSegment.at(sender_qq) + f"\n标题:{title}\nPID:{pid}\n作者:{author}")
                await setu.finish(MessageSegment.image(f"{url}"))
            except MatcherException:
                raise
            except Exception as e:
                await setu.finish(f"发生错误：{e}")
    elif config.api_url == 1:
        if tag := args.extract_plain_text():
            try:
                sender_qq = event.get_user_id()
                response = await http_client.get(f"https://image.anosu.top/pixiv/json?keyword={tag}")
                json_dict = response.json()
                title = json_dict[0]["title"]
                pid = json_dict[0]["pid"]
                author = json_dict[0]["user"]
                url = json_dict[0]["url"]
                await setu.send(MessageSegment.at(sender_qq)+f"\n标题:{title}\nPID:{pid}\n作者:{author}")
                await setu.finish(MessageSegment.image(f"{url}"))
            except MatcherException:
                raise
            except Exception as e:
                await setu.finish(f"发生错误：{e}")
        else:
            try:
                sender_qq = event.get_user_id()
                response = await http_client.get("https://image.anosu.top/pixiv/json")
                json_dict = response.json()  # 注意：这里可能需要异常处理
                title = json_dict[0]["title"]
                pid = json_dict[0]["pid"]
                author = json_dict[0]["user"]
                url = json_dict[0]["url"]
                await setu.send(MessageSegment.at(sender_qq) + f"\n标题:{title}\nPID:{pid}\n作者:{author}")
                await setu.finish(MessageSegment.image(f"{url}"))
            except MatcherException:
                raise
            except Exception as e:
                await setu.finish(f"发生错误：{e}")

leg = on_command("leg", aliases={"腿子", "来份腿子"})

@leg.handle()
async def handle_function(event: MessageEvent, args: Message = CommandArg()):
    # 提取参数纯文本作为地名，并判断是否有效
    try:
        sender_qq_leg = event.get_user_id()
        response_leg = await http_client.get("https://api.lolimi.cn/API/meizi/api.php?type=json")
        json_dict_leg = response_leg.json()
        image_leg = json_dict_leg["text"]
        at_segment_leg = MessageSegment.at(user_id=sender_qq_leg)
        await setu.send(at_segment_leg)
        await setu.finish(MessageSegment.image(image_leg))
    except MatcherException:
        raise
    except Exception as e:
        await leg.finish(f"发生错误：{e}")

girl = on_command("girl", aliases={"少女写真", "来份写真"})

@girl.handle()
async def handle_function(event: MessageEvent, args: Message = CommandArg()):
    # 提取参数纯文本作为地名，并判断是否有效
    try:
        sender_qq_girl = event.get_user_id()
        response_girl = await http_client.get("https://api.lolimi.cn/API/meinv/api.php?type=json")
        json_dict_girl = response_girl.json()
        image_girl = json_dict_girl["data"]["image"]
        at_segment_girl = MessageSegment.at(user_id=sender_qq_girl)
        await girl.send(at_segment_girl)
        await girl.finish(MessageSegment.image(image_girl))
    except MatcherException:
        raise
    except Exception as e:
        await girl.finish(f"发生错误：{e}")