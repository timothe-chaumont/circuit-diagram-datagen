import os
from dotenv import load_dotenv


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
        circuitikz_str += f"\\draw {s['from']} to[{s['type']}] {s['to']};\n"
    return BEFORE_LATEX + circuitikz_str + AFTER_LATEX


def save_to_latex(latex_string, filename="file") -> None:
    """Saves string to a .tex file"""
    with open(f"{filename}.tex", 'w') as f:
        f.write(latex_string)


def latex_to_jpg(latex_filename: str, latex_path: str, ghostscript_path: str) -> None:
    # create a pdf from the latex file
    os.system(os.path.join(latex_path, "latex") +
              f" {latex_filename}.tex -output-format=pdf --interaction=batchmode")
    # convert them into images
    os.system(os.path.join(ghostscript_path, "gswin64c") +
              f" -dNOPAUSE -sDEVICE=jpeg -r200 -dJPEGQ=60 -sOutputFile={latex_filename}-%03d.jpg {latex_filename}.pdf -dBATCH")
    # delete unneeded files
    for extension in ("tex", "aux", "log", "pdf"):
        os.remove(f"{latex_filename}.{extension}")


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
