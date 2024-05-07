from typing import Generator
import cv2


def resize(
    pipe: Generator[dict, None, None], 
    *, 
    width: int, 
    height: int, 
    image_key: str = 'main.image', 
    preserve_aspect: bool = True
) -> Generator[dict, None, None]:
    """Image processing operator that resizes the input image to the specified size.

    The image is looked up in the dict using the 'image_key' parameter. It is split into
    a list by the '.' and looked up recursively.

    If 'preserve_aspect' is True, the aspect ratio of the image is preserved and pasted into
    a black image of the requested size.
    """

    print("Building picamkit.ops.imaging.resize")
    print(f"- image_key: {image_key}")
    print(f"- width: {width}")
    print(f"- height: {height}")
    print(f"- preserve_aspect: {preserve_aspect}")

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


def scale(
    pipe: Generator[dict, None, None], 
    *, 
    factor: float, 
    image_key: str = 'main.image'
) -> Generator[dict, None, None]:
    """Image processing operator that scales the input image by the specified factor.

    The image is looked up in the dict using the 'image_key' parameter. It is split into
    a list by the '.' and looked up recursively.
    """

    print("Building picamkit.ops.imaging.scale")
    print(f"- image_key: {image_key}")
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

