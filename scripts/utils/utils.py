import hashlib
import os
from dotenv import load_dotenv
from subprocess import call, DEVNULL


# latex commands around the circuitikz commands
BEFORE_LATEX = r"""\documentclass[convert={density=100}]{standalone}
\usepackage{circuitikz}
\standaloneenv{circuitikz}
\begin{document}
\begin{circuitikz}"""
AFTER_LATEX = r"""\end{circuitikz}
\end{document}"""


def load_env_var():
    """Returns environment variables from .env file"""
    load_dotenv()
    latex_path = os.environ.get('LATEX_PATH')
    ghostscript_path = os.environ.get('GS_PATH')
    return latex_path, ghostscript_path


def read_tokens(filename="tokens.lst"):
    """Returns a list of all tokens corresponding
       duplicates will be removed.
    """
    with open(filename, "r") as f:
        data = [l.replace("\n", "").strip() for l in f.readlines()]
    return data


def create_dictionnaries(tokens):
    """Returns two dictionnaries of all tokens and their
       corresponding index.
    """
    token_to_idx = {t: i for i, t in enumerate(tokens)}
    idx_to_token = {i: t for i, t in enumerate(tokens)}
    return token_to_idx, idx_to_token


def segment_list_to_latex(segments_list):
    """Converts list of elements to latex.

    Generates latex (circuitikz code) for a given descrition of an electrical circuit
    Takes a circuit represented by a list of segment as input.

    Args:
        segments_list: a list of dictionnaries (later objects) describing an electrical circuit.

    Returns:
        A string representing circuitikz instructions"""
    circuitikz_str = ""
    for s in segments_list:
        if s.label:
            circuitikz_str += f"\\draw {s.from_pos} to[{s.type}, l={s.label}] {s.to_pos};\n"
        else:
            circuitikz_str += f"\\draw {s.from_pos} to[{s.type}] {s.to_pos};\n"
    return BEFORE_LATEX + circuitikz_str + AFTER_LATEX


def save_to_latex(latex_string: str,  save_path: str = "data", filename: str = "file") -> None:
    """Saves string to a .tex file"""
    with open(os.path.join(save_path, f"{filename}.tex"), 'w') as f:
        f.write(latex_string)


def latex_to_jpg(latex_filename: str, latex_path: str, ghostscript_path: str, save_path: str = "data",) -> None:
    tex_file_path = os.path.join(save_path, latex_filename)
    # create a pdf from the latex file
    os.system(os.path.join(latex_path, "latex") +
              f" {tex_file_path}.tex -output-format=pdf --interaction=batchmode --output-directory={save_path} --aux-directory={save_path}")
    # convert them into images
    call(os.path.join(ghostscript_path, "gswin64c") +
         f" -dNOPAUSE -sDEVICE=jpeg -r200 -dJPEGQ=60 -sOutputFile={tex_file_path}.jpg {tex_file_path}.pdf -dBATCH -dQUIET", stdout=DEVNULL)
    # os.system(os.path.join(ghostscript_path, "gswin64c") +
    #           f" -dNOPAUSE -sDEVICE=jpeg -r200 -dJPEGQ=60 -sOutputFile={tex_file_path}-%03d.jpg {tex_file_path}.pdf -dBATCH")
    # delete unneeded files
    for extension in ("tex", "aux", "log", "pdf"):
        os.remove(f"{tex_file_path}.{extension}")


def get_image_name(circuit_latex_string: str) -> str:
    name = hashlib.sha1(circuit_latex_string.encode('utf-8')).hexdigest()[:15]
    return name


if __name__ == '__main__':
    # simple test
    import random as rd
    from os.path import dirname, abspath, join

    # load env variables from .env file
    latex_path, ghostscript_path = load_env_var()

    # read all tokens
    filepath = join(dirname(dirname(dirname(abspath(__file__)))), "tokens.lst")
    tokens_list = read_tokens(filepath)
    token_to_idx, idx_to_token = create_dictionnaries(tokens_list)

    gen_circuit = [{'from': (0, 0), 'to': (2, 0), 'type': 'ammeter'}, {'from': (2, 0), 'to': (4, 0), 'type': 'battery1'}, {'from': (0, 0), 'to': (0, 6), 'type': 'short'},
                   {'from': (0, 6), 'to': (4, 6), 'type': 'generic'}, {'from': (4, 6), 'to': (4, 0), 'type': 'short'}]
    latex_string = segment_list_to_latex(gen_circuit)
    save_to_latex(latex_string)
    latex_to_jpg("file", latex_path, ghostscript_path)
