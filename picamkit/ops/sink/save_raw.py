import os
import cv2
import numpy as np


bayer_codes = {
    'SBGGR16': cv2.COLOR_BayerBGGR2BGR,
    'SGRBG16': cv2.COLOR_BayerGRBG2BGR,
    'SGBRG16': cv2.COLOR_BayerGBRG2BGR,
    'SRGGB16': cv2.COLOR_BayerRGGB2BGR,
}

def save_raw(pipe, outdir, *, image_key='raw.image', format_key='raw.format', prefix='img'):
    
    print("Building picamkit.ops.io.save_raw")
    print(f"- outdir: {outdir}")
    print(f"- image_key: {image_key}")
    print(f"- format_key: {format_key}")
    print(f"- prefix: {prefix}")
    
    os.makedirs(outdir, exist_ok=True)

    image_keys = image_key.split('.')
    format_keys = format_key.split('.')
    
    def gen():
        for items in pipe:
            if not isinstance(items, list):
                items = [items]
        
            for item in items:
                idx = item['idx']
        
                image = item
                for key in image_keys:
                    image = image[key]
                image_format = item
                for key in format_keys:
                    image_format = image_format[key]

                # saving
                if name := item.get('name', None):
                    img_path = os.path.join(outdir, f"{prefix}-{idx:04d}-{name}-raw.png")
                else:
                    img_path = os.path.join(outdir, f"{prefix}-{idx:04d}-raw.png")

                print(f"Saving {img_path}")

                # demosaic and save the image
                bayer_code = bayer_codes[image_format]
                image = cv2.demosaicing(image, bayer_code)
                cv2.imwrite(img_path, image)
        
                yield item

    return gen()


def save_raw8(pipe, outdir, *, image_key='raw.image', format_key='raw.format', prefix='img'):
    
    print("Building picamkit.ops.io.save_raw8")
    print(f"- outdir: {outdir}")
    print(f"- image_key: {image_key}")
    print(f"- format_key: {format_key}")
    print(f"- prefix: {prefix}")

    os.makedirs(outdir, exist_ok=True)

    image_keys = image_key.split('.')
    format_keys = format_key.split('.')

    def gen():
        for items in pipe:
            if not isinstance(items, list):
                items = [items]
        
            for item in items:
                idx = item['idx']
        
                image = item
                for key in image_keys:
                    image = image[key]
                image_format = item
                for key in format_keys:
                    image_format = image_format[key]

                # saving
                if name := item.get('name', None):
                    img_path = os.path.join(outdir, f"{prefix}-{idx:04d}-{name}-raw8.png")
                else:
                    img_path = os.path.join(outdir, f"{prefix}-{idx:04d}-raw8.png")

                print(f"Saving {img_path}")

                # demosaic the image
                bayer_code = bayer_codes[image_format]
                image = cv2.demosaicing(image, bayer_code)

                # subtract the sensor black levels
                # TODO: need to grab this from the metadata file
                image = np.maximum(image, 4096) - 4096

                # apply the gamma encoding and convert to 8bit range
                image = np.power(image, 1.0/2.2) / np.power(65536, 1.0/2.2) * 255
                image = image.astype(np.uint8)

                # save the image
                cv2.imwrite(img_path, image)
        
                yield item

    return gen()

