import ddddocr
import uvicorn
import base64
from io import BytesIO
from PIL import Image
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

description = """
* 增强版DDDDOCR

* 识别效果完全靠玄学，可能可以识别，可能不能识别。——DDDDOCR

  <img src="https://img.shields.io/badge/GitHub-ffffff"></a> <a href="https://github.com/81NewArk/StupidOCR"> <img src="https://img.shields.io/github/stars/81NewArk/StupidOCR?style=social"> <img src="https://badges.pufler.dev/visits/81NewArk/StupidOCR">
"""


app = FastAPI(title="StupidOCR", description=description, version="1.0.8")
app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ocr = ddddocr.DdddOcr(show_ad=False, beta=True)
number_ocr = ddddocr.DdddOcr(show_ad=False, beta=True)
number_ocr.set_ranges(0)
compute_ocr = ddddocr.DdddOcr(show_ad=False, beta=True)
compute_ocr.set_ranges("0123456789+-x÷=")
alphabet_ocr = ddddocr.DdddOcr(show_ad=False, beta=True)
alphabet_ocr.set_ranges(3)
det = ddddocr.DdddOcr(det=True,show_ad=False)
shadow_slide = ddddocr.DdddOcr(det=False, ocr=False,show_ad=False)

class ModelImageIn(BaseModel):
    img_base64: str

class ModelSliderImageIn(BaseModel):
    gapimg_base64: str
    fullimg_base64: str






@app.get("/",summary="index.html",tags=["主页"])
async def read_root():
    return FileResponse("dist/index.html")


@app.post("/api/ocr/image", summary="通用", tags=["验证码识别"])
async def ocr_image(data: ModelImageIn):
    img = base64.b64decode(data.img_base64)
    result = ocr.classification(img)
    return {"result": result}

@app.post("/api/ocr/number", summary="数字", tags=["验证码识别"])
async def ocr_image_number(data: ModelImageIn):
    img = base64.b64decode(data.img_base64)
    result = number_ocr.classification(img, probability=True)
    string = "".join(result['charsets'][i.index(max(i))] for i in result['probability'])
    return {"result": string}

@app.post("/api/ocr/compute", summary="算术", tags=["验证码识别"])
async def ocr_image_compute(data: ModelImageIn):
    img = base64.b64decode(data.img_base64)
    result = compute_ocr.classification(img, probability=True)
    string = "".join(result['charsets'][i.index(max(i))] for i in result['probability'])
    string = string.split("=")[0].replace("x", "*").replace("÷", "/")
    try:
        result = eval(string)
    except:
        result = "Error"
    return {"result": result}

@app.post("/api/ocr/alphabet", summary="字母", tags=["验证码识别"])
async def ocr_image_alphabet(data: ModelImageIn):
    img = base64.b64decode(data.img_base64)
    result = alphabet_ocr.classification(img, probability=True)
    string = "".join(result['charsets'][i.index(max(i))] for i in result['probability'])
    return {"result": string}

@app.post("/api/ocr/detection", summary="文字点选", tags=["验证码识别"])
async def ocr_image_det(data: ModelImageIn):
    img = base64.b64decode(data.img_base64)
    img_pil = Image.open(BytesIO(img))
    res = det.detection(img)
    result = {ocr.classification(img_pil.crop(box)): [box[0] + (box[2] - box[0]) // 2, box[1] + (box[3] - box[1]) // 2] for box in res}
    return {"result": result}

@app.post("/api/ocr/slider/gap", summary="缺口滑块识别", tags=["验证码识别"])
async def ocr_image_slider_gap(data: ModelSliderImageIn):
    gapimg = base64.b64decode(data.gapimg_base64)
    fullimg = base64.b64decode(data.fullimg_base64)
    result = det.slide_match(gapimg, fullimg)
    return {"result": result}

@app.post("/api/ocr/slider/shadow", summary="阴影滑块识别", tags=["验证码识别"])
async def ocr_image_slider_shadow(data: ModelSliderImageIn):
    shadowimg = base64.b64decode(data.gapimg_base64)
    fullimg = base64.b64decode(data.fullimg_base64)
    result = shadow_slide.slide_comparison(shadowimg, fullimg)
    return {"result": result}

if __name__ == '__main__':
    print('''

      _____   _                     _       _    ____     _____   _____  
     / ____| | |                   (_)     | |  / __ \   / ____| |  __  \ 
    | (___   | |_   _   _   _ __    _    __| | | |  | | | |      | |__) |
     \___ \  | __| | | | | | '_ \  | |  / _` | | |  | | | |      |  _  / 
     ____) | | |_  | |_| | | |_) | | | | (_| | | |__| | | |____  | | \  \ 
    |_____/   \__|  \__,_| | .__/  |_|  \__,_|  \____/   \_____| |_|  \_/
                           | |                                           
                           |_|                                           


                    软件主页：http://127.0.0.1:6688
                    开发文档：http://localhost:6688/docs
                   

                    代码编写：81NewArk

       ''')

    uvicorn.run(app, host="0.0.0.0", port=6688, access_log=True)
