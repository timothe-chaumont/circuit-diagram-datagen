import cv2
from typing import Tuple

WHITE = (255, 255, 255)


def pad_images(img: str, output_size: Tuple[int, int] = (1000, 1000)):
    """Reads and pads an image with white pixels to a given size.
        Image should be smaller than the desired output size
    """
    old_img = cv2.imread(img)
    assert old_img.shape[0] <= output_size[0] and old_img.shape[1] <= output_size[1], \
        f"Image should be smaller than {output_size}, but is {tuple(old_img.shape[:2])}"

    # compute the padding values
    delta_width = output_size[1] - old_img.shape[1]
    delta_height = output_size[0] - old_img.shape[0]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_height, delta_height - pad_height,
               pad_width, delta_width - pad_width)
    # apply padding
    new_img = cv2.copyMakeBorder(
        old_img, *padding, borderType=cv2.BORDER_CONSTANT, value=WHITE)
    return new_img
