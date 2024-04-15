import cv2


def resize(pipe, *, width, height, image_key='main.image', preserve_aspect=True):
    print("Building picamkit.ops.imaging.resize")
    print(f"- image key: {image_key}")
    print(f"- width: {width}")
    print(f"- height: {height}")
    print(f"- preserve aspect: {preserve_aspect}")

    image_keys = image_key.split('.')

    def gen():
        for item in pipe:
            image_item = None
            image = item
            for key in image_keys:
                image_item = image
                image = image[key]

            iheight, iwidth, _ = image.shape
            fx = width / iwidth
            fy = height / iheight

            if preserve_aspect:
                fx = fy = min(fx, fy)
        
            image = cv2.resize(image, None, fx=fx, fy=fy)

            iheight, iwidth, _ = image.shape
            if iheight < height or iwidth < width:
                top = int((height - iheight)/2)
                bottom = height - iheight - top
                left = int((width - iwidth)/2)
                right = width - iwidth - left
            
                image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0)
        
            image_item[image_keys[-1]] = image
                
            yield item

    return gen()


def scale(pipe, *, factor, image_key='main.image'):
    print("Building picamkit.ops.imaging.scale")
    print(f"- image key: {image_key}")
    print(f"- factor: {factor}")

    image_keys = image_key.split('.')

    def gen():
        for item in pipe:
            image_item = None
            image = item
            for key in image_keys:
                image_item = image
                image = image[key]
        
            image_item[image_keys[-1]] = cv2.resize(image, None, fx=factor, fy=factor)

            yield item

    return gen()

