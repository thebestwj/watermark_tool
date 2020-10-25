from PIL import Image, ImageDraw, ImageFont
import os

# font path, such as 'C:/windows/fonts/Arial.ttf'
watermark_font = 'C:/windows/fonts/Bradhitc.ttf'
# image format
support_formats = ['.jpg', '.png']
# custom text
watermark_text = 'a cat lover'
# size
watermark_size = 1.2

def judge_color(img):
    """
    judge the main color of the image(dark/light)
    :param img: image to be judged
    :return: 0 = light 1 = dark
    """
    color_list = img.load()
    x, y = img.size
    r, g, b = 0, 0, 0
    for i in range(0, x):
        for j in range(0, y):
            r += color_list[i, j][0]
            g += color_list[i, j][1]
            b += color_list[i, j][2]
    r /= x * y
    g /= x * y
    b /= x * y
    # print main color
    print(('#' + hex(int(r))[-2:] + hex(int(g))[-2:] + hex(int(b))[-2:]).replace("x", "0"))
    if r * 0.299 + g * 0.578 + b * 0.114 >= 192:
        # light
        return 0
    else:
        # dark
        return 1


def add_watermark(name, img, text):
    """
    add watermark to an image
    :param name: name of the image
    :param img: image
    :param text: watermark text
    :return: modified image
    """
    draw = ImageDraw.Draw(img)
    width, height = img.size
    scale = int(max(width, height) / 30 * watermark_size) 
    font = ImageFont.truetype(watermark_font, size=scale)

    judge = judge_color(img.crop((width - scale * len(text) / 2, height - scale * 2, width, height)))
    if judge == 1:
        fillcolor = '#ffffff'
        watermark_type = 'light watermark'
    else:
        fillcolor = '#000000'
        watermark_type = 'dark watermark'
    draw.text((width - scale * len(text) / 2, height - scale * 2), text, font=font, fill=fillcolor)
    print('image = %s,%s size = %d*%d,scale = %d' % (name, watermark_type, width, height, scale))
    return img


if __name__ == '__main__':

    # search files in cwd
    files = os.listdir(os.getcwd())
    image_files = []

    for file in files:
        file_format = file.lower()[-4:]
        if file_format in support_formats:
            image_files.append((file, file_format))
    print(image_files)

    # mkdir for output if not exist
    if not os.path.exists('out'):
        os.makedirs('out')

    for n, f in image_files:
        image = Image.open(n)
        image = add_watermark(n, image, watermark_text)
        image.save('out/' + n, 'jpeg')
