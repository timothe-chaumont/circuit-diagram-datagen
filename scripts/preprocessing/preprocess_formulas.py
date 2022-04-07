from typing import List
import re


def basic_tokenize(formula: str) -> List[str]:
    """Returns a list of tokens corresponding to the input formula.
        This basic version splits formulas on spaces. Those formulas are generated accordingly. 
    """
    return re.findall(r"to\[[\w\s]+\]|[a-z0-9\\]+|\([0-9|\s,]+\)|;", formula)


if __name__ == "__main__":
    formula = r"\draw (5, 3) to[capacitor] (5, 5); \draw (7, 3) to[short] (7, 5); \draw (5, 5) to[capacitor] (7, 5); \draw (3, 3) to[short] (5, 3); \draw (7, 0) to[generic] (7, 3); \draw (0, 0) to[european current source] (3, 0); \draw (5, 0) to[short] (7, 0);"
    tokens = basic_tokenize(formula)
    print(tokens)
