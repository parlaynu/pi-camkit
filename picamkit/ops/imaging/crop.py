from typing import Generator


def centre_crop(
    pipe: Generator[dict, None, None], 
    *, 
    factor: float, 
    image_key: str = 'main.image'
) -> Generator[dict, None, None]:
    """Image processing operator that crops the centre portion of the input image by the specified factor.

    The image is looked up in the dict using the 'image_key' parameter. It is split into
    a list by the '.' and looked up recursively.
    """

    print("Building picamkit.ops.imaging.centre_crop")
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
        
            height, width, *_ = image.shape
            
            hstart = (height - int(height*factor)) // 2
            hend = height - hstart
            
            wstart = (width - int(width*factor)) // 2
            wend = width - wstart
            
            image_item[image_keys[-1]] = image[hstart:hend, wstart:wend, ...]

            yield item

    return gen()

