import click

import scripts.utils.utils as ut
import scripts.data_generation.generate_circuits as gc


@click.command()
@click.option('--nb_images', default=1, help='Number of images to generate')
@click.option('--save_to', default="data", help="Path where to save the images")
def generate(nb_images: int, save_to: str) -> None:
    """Uses various functions to generate circuit data

    Args:
        nb_images (int): Number of images to generate
        save_to (str): Path where to save the generated images
    """
    latex_path, ghostscript_path = ut.load_env_var()

    for i in range(nb_images):
        segments_list = gc.generate_v2()
        latex_string = ut.segment_list_to_latex(segments_list)
        filename = f"file-{i}"

        ut.save_to_latex(latex_string, save_to, filename)
        ut.latex_to_jpg(filename, latex_path, ghostscript_path, save_to)

    click.echo(f"Generated {nb_images} images.")


if __name__ == '__main__':
    generate()
