import click
import os

import scripts.utils.utils as ut
import scripts.utils.image_utils as iu
import scripts.data_generation.generate_circuits as gc


@click.command()
@click.option('--nb_images', default=1, help='Number of images to generate')
@click.option('--save_to', default="data", help="Path where to save the images")
def main(nb_images: int, save_to: str) -> None:
    """Uses various functions to generate circuit data

    Args:
        nb_images (int): Number of images to generate
        save_to (str): Path where to save the generated images
    """
    latex_path, ghostscript_path = ut.load_env_var()
    circuit_generator = gc.CircuitGenerator()
    images_folder_path = os.path.join(save_to, "circuit_images")

    for i in range(nb_images):
        segments_list = circuit_generator.generate_one_circuit()
        latex_string = ut.segment_list_to_latex(segments_list)
        filename = ut.get_image_name(latex_string)

        ut.save_to_latex(ut.BEFORE_LATEX + latex_string + ut.AFTER_LATEX,
                         images_folder_path, filename)
        ut.latex_to_jpg(filename, latex_path,
                        ghostscript_path, images_folder_path)
        # pad, resize and save the image
        img_path = os.path.join(images_folder_path, f"{filename}.jpg")
        img = iu.read_image(img_path)
        img = iu.pad_to_square(img, border=50)
        img = iu.resize_image(img, (350, 350))
        iu.save_image(img, img_path)

        # find the first empty line
        with open(os.path.join(save_to, "circuitikz_code.lst"), "r") as f:
            line_number = 1
            for line in f:
                line_number += 1
                if line == "\n":
                    break

        # save its name and line TODO
        with open(os.path.join(save_to, "circuit2latex_train.lst"), "a") as f:
            f.write(f"{line_number} {filename}\n")

        # save the formula
        with open(os.path.join(save_to, "circuitikz_code.lst"), "a") as f:
            f.write(f"{latex_string}\n")

    click.echo(f"Generated {nb_images} images.")


if __name__ == '__main__':
    main()
