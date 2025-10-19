from pygame import BLEND_RGBA_MULT


def create_alpha_image(image, alpha):
    """创建具有指定透明度的图像副本"""
    alpha_image = image.copy()
    alpha_image.fill((255, 255, 255, alpha), None, BLEND_RGBA_MULT)
    return alpha_image
