import os

# latex commands around the circuitikz commands
BEFORE_LATEX = r"""\documentclass[convert={density=100}]{standalone}
\usepackage{circuitikz}
\standaloneenv{circuitikz}
\begin{document}
\begin{circuitikz}"""
AFTER_LATEX = r"""\end{circuitikz}
\end{document}"""


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


if __name__ == '__main__':
    # simple test
    import random as rd
    from os.path import dirname, abspath, join

    # read all tokens
    filepath = join(dirname(dirname(dirname(abspath(__file__)))), "tokens.lst")
    tokens_list = read_tokens(filepath)
    token_to_idx, idx_to_token = create_dictionnaries(tokens_list)

    gen_circuit = [{'from': (0, 0), 'to': (2, 0), 'type': 'ammeter'}, {'from': (2, 0), 'to': (4, 0), 'type': 'battery1'}, {'from': (0, 2), 'to': (2, 2), 'type': 'short'},
                   {'from': (0, 0), 'to': (0, 2), 'type': 'ammeter'}, {'from': (2, 0), 'to': (2, 2), 'type': 'voltmeter'}, {'from': (2, 2), 'to': (2, 4), 'type': 'short'}, {'from': (2, 4), 'to': (2, 6), 'type': 'short'}]
    latex_string = segment_list_to_latex(gen_circuit)
    save_to_latex(latex_string)
