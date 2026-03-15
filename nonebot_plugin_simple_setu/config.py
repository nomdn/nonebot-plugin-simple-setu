from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    #setu功能 1为开启0为关闭
    simple_setu_enable :int=1
    #at获取腿子图 1为开启0为关闭
    simple_setu_on_keyword_leg_enable :int=1
    #图片代理地址，默认为空，开启后会将图片链接替换为代理链接
    simple_setu_image_proxy :str = ""
