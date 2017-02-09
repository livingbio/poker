from PIL import Image
import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
tool = tools[0]

def ocr(path):
    img = Image.open(path).crop((565, 185, 710, 230))

    txt = tool.image_to_string(
        img,
        lang='eng',
        builder=pyocr.builders.TextBuilder()
    )
    return txt