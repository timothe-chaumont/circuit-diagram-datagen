import cv2
from typing import Tuple
import numpy as np

WHITE = 255


def read_image(img: str) -> np.ndarray:
    return cv2.imread(img, cv2.IMREAD_GRAYSCALE)


def pad_image(img: np.ndarray, output_size: Tuple[int, int] = (1000, 1000)) -> np.ndarray:
    """Reads and pads an image with white pixels to a given size.
        Image should be smaller than the desired output size.
        Not used anymore.
    """
    assert img.shape[0] <= output_size[0] and img.shape[1] <= output_size[1], \
        f"Image should be smaller than {output_size}, but is {tuple(img.shape[:2])}"

    # compute the padding values
    delta_width = output_size[1] - img.shape[1]
    delta_height = output_size[0] - img.shape[0]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_height, delta_height - pad_height,
               pad_width, delta_width - pad_width)
    # apply padding
    new_img = cv2.copyMakeBorder(
        img, *padding, borderType=cv2.BORDER_CONSTANT, value=WHITE)
    return new_img


def pad_to_square(img: np.ndarray, border: int = 50) -> np.ndarray:
    """ Adds white pixels on the smallest dimension to make it square.
        Add also a border of white pixels around the image.
    """
    height, width = img.shape[:2]
    max_length = max(height, width)
    pad_left = (max_length - width) // 2
    pad_right = (max_length - width) - pad_left
    pad_top = (max_length - height) // 2
    pad_bottom = (max_length - height) - pad_top
    padding = (pad_top + border, pad_bottom + border,
               pad_left + border, pad_right + border)
    new_img = cv2.copyMakeBorder(
        img, *padding, borderType=cv2.BORDER_CONSTANT, value=WHITE)
    return new_img


def resize_image(img: np.ndarray) -> np.ndarray:
    return cv2.resize(img, (300, 300), interpolation=cv2.INTER_LANCZOS4)


def show_image(img: np.ndarray, title: str = "Image") -> None:
    cv2.imshow(title, img)
    cv2.waitKey(0)


if __name__ == '__main__':
    img_path = r"..\..\data\file-0-001.jpg"
    img = pad_to_square(read_image(img_path))
    img = resize_image(img)
    show_image(img)
