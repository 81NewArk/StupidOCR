import uvicorn
from fastapi import FastAPI, Body
import base64
import ddddocr
from io import BytesIO
from PIL import Image

'''
pip install uvicorn
pip install fastapi
pip install base64
pip install ddddocr
'''

app = FastAPI(title='StupidOCR 开发文档', description='代码编写：81NewArk', version="1.0.5")


@app.post("/identify_GeneralCAPTCHA", summary='识别图片内文字', description='普通图片验证码识别，上传图片的Base64编码', tags=['图片验证码识别'])
async def identify_GeneralCAPTCHA(ImageBase64: str = Body(..., title='验证码图片Bse64文本', embed=True)):
    base64_data = base64.b64decode(ImageBase64)
    ocr = ddddocr.DdddOcr(show_ad=False)
    res = ocr.classification(base64_data)
    return {"result": res,
            "Blog": "https://Niuer-Pepsi.lofter.com"}


@app.post("/identify_ArithmeticCAPTCHA", summary='识别算术验证码', description='算术题验证码识别，上传图片的Base64编码，提供两个返回，自行取值分割文本并识别',
          tags=['图片验证码识别'])
async def identify_ArithmeticCAPTCHA(ImageBase64: str = Body(..., title='验证码图片Bse64文本', embed=True)):
    base64_data = base64.b64decode(ImageBase64)
    ocr = ddddocr.DdddOcr(show_ad=False)
    res = ocr.classification(base64_data)

    zhi = "Calculation error"
    if "+" or '-' or 'x' or '/' not in res:
        zhi = "Calculation error"
    if '+' in res:
        zhi = int(res.split('+')[0]) + int(res.split('+')[1][:-1])
    if '-' in res:
        zhi = int(res.split('-')[0]) - int(res.split('-')[1][:-1])
    if 'x' in res:
        zhi = int(res.split('x')[0]) * int(res.split('x')[1][:-1])
    if '/' in res:
        zhi = int(res.split('/')[0]) / int(res.split('/')[1][:-1])

    return {"solution_result": zhi,
            "raw_result": res,
            "Blog": "https://Niuer-Pepsi.lofter.com"
            }


@app.post("/SliderMode_AloneGap", summary='缺口为滑动的单独图片，返回坐标', description='识别模型1：缺口图片为单独图片', tags=['滑块验证码识别'])
async def SliderMode_AloneGap(Gap_ImageBase64: str = Body(..., title='滑块缺口图片的Bse64文本', embed=True),
                              Background_ImageBase64: str = Body(..., title='背景图片的Bse64文本', embed=True)):
    ocr = ddddocr.DdddOcr(show_ad=False)
    res = ocr.slide_match(base64.b64decode(Gap_ImageBase64), base64.b64decode(Background_ImageBase64),
                          simple_target=True)
    print(res)
    return {"result": res,
            "Blog": "https://Niuer-Pepsi.lofter.com"}


@app.post("/SliderMode_Comparison", summary='缺口原图和完整原图识别，无单独滑动的缺口图片，返回坐标', description='识别模型2：一张为有缺口原图，一张为完整原图',
          tags=['滑块验证码识别'])
async def SliderMode_Comparison(HaveGap_ImageBase64: str = Body(..., title='拥有缺口图片的Bse64文本', embed=True),
                                Full_ImageBase64: str = Body(..., title='完整背景图片的Bse64文本', embed=True)):
    ocr = ddddocr.DdddOcr(det=False, ocr=False)
    res = ocr.slide_comparison(base64.b64decode(HaveGap_ImageBase64), base64.b64decode(Full_ImageBase64))
    return {"result": res,
            "Blog": "https://Niuer-Pepsi.lofter.com"}


@app.post("/ClickChoice_CAPTCHA", summary='汉字点选验证码', description='点选识别返回坐标', tags=['文字点选验证码识别'])
async def ClickChoice_CAPTCHA(ClickChoice_ImageBase64: str = Body(..., title='点选图片的Base64编码', embed=True)):
    ocr1 = ddddocr.DdddOcr(show_ad=False)
    ocr2 = ddddocr.DdddOcr(det=True, show_ad=False)

    res = ocr2.detection(base64.b64decode(ClickChoice_ImageBase64))
    if __name__ == '__main__':
        img = Image.open(BytesIO(base64.b64decode(ClickChoice_ImageBase64)))
        res = ocr2.detection(base64.b64decode(ClickChoice_ImageBase64))
        result = {}
        for box in res:
            x1, y1, x2, y2 = box

            result[ocr1.classification(img.crop(box))] = [x1 + ((y1 - x1) // 2), x2 + ((y2 - x2) // 2)]  # 文字位置

    return {"result": result,
            "Blog": "https://Niuer-Pepsi.lofter.com"}


@app.get("http://Niuer-Pepsi.lofter.com", summary='欢迎关注作者的乐乎博客', description='求一键三连，我想混个乐乎认证',
         tags=['关于作者：81NewArk【我叫牛二】'])
def Niuer():
    return {"Blog": "Niuer-Pepsi.lofter.com"}


@app.get("https://space.bilibili.com/37887820", summary='视频教程自己找', description='记得给三连', tags=['关于作者：81NewArk【我叫牛二】'])
def Pepsi():
    return {"Blog": "https://space.bilibili.com/37887820"}


@app.get("https://github.com/sml2h3/ddddocr", summary='奉行着开箱即用、最简依赖理念的Python库',
         description='ddddocr是由sml2h3开发的专为验证码厂商进行对自家新版本验证码难易强度进行验证的一个python库，其由作者与kerlomz共同合作完成，通过大批量生成随机数据后进行深度网络训练，本身并非针对任何一家验证码厂商而制作，本库使用效果完全靠玄学，可能可以识别，可能不能识别。',
         tags=['项目依赖：DDDDOCR'])
def dddd():
    return {"Github": "https://github.com/sml2h3/ddddocr"}


if __name__ == '__main__':
    print("")
    print("")
    print("   _____   _                             _        ____     _____   _____  ")
    print("  / ____| | |                   (_)     | |      / __ \   / ____| |  __ \ ")
    print(" | (___   | |_   _   _   _ __    _    __| |     | |  | | | |      | |__) |")
    print("  \___ \  | __| | | | | | '_ \  | |  / _` |     | |  | | | |      |  _  / ")
    print("  ____) | | |_  | |_| | | |_) | | | | (_| |  _  | |__| | | |____  | | \ \ ")
    print(" |_____/   \__|  \__,_| | .__/  |_|  \__,_| (_)  \____/   \_____| |_|  \_/")
    print("                        | |                                               ")
    print("                        |_|                                               ")
    print("")
    print("")
    print("                 开发者文档：http://127.0.0.1:6688/docs          ")
    print("                 开发者文档：http://localhost:6688/docs          ")
    print("                 项目依赖：FastAPI+ Uvicorn + DDDDOCR            ")
    print("")
    print("                 乐乎博客：https://Niuer-Pepsi.lofter.com        ")
    print("                 代码编写：81NewArk                              ")
    print("")
    print("")
    print("")
    print("")

    uvicorn.run(app, port=6688, host="0.0.0.0")
