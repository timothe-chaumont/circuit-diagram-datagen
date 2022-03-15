import click

import scripts.utils.utils as ut
import scripts.data_generation.generate_circuits as gc


@click.command()
@click.option('--nb_images', default=1, help='Number of images to generate')
def generate(nb_images: int):
    """Uses various functions to generate circuit data

    Args:
        nb_images (int): Number of images to generate
    """
    latex_path, ghostscript_path = ut.load_env_var()

    for i in range(nb_images):
        segments_list = gc.generate_one_loop_circuit()
        latex_string = ut.segment_list_to_latex(segments_list)
        filename = f"file-{i}"

        ut.save_to_latex(latex_string, filename)
        ut.latex_to_jpg(filename, latex_path, ghostscript_path)
        
    click.echo(f"Generated {nb_images} images.")


if __name__ == '__main__':
    generate()
