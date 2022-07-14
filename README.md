# Circuit-diagram-datagen

Python script that generates circuit diagrams data : [CircuiTikz](https://ctan.org/pkg/circuitikz) (LaTeX) and the corresponding image.

_Its purpose is to create data to train machine learning models._

## Steps to generate data (Windows)

1. Install the dependencies with `make install` (possibly in a virtual environment)
2. Install [LaTeX](https://www.latex-project.org/get/)
3. Install [Ghostscript](https://ghostscript.com/releases/gsdnld.html)
4. Create a file called _.env_ containing paths to `latex.exe` and `gswin64c.exe` binaries, in the same way as [_example.env_](/example.env).
5. Run `make generate` in a cmd window from the root directory

---
The [circuit-to-latex](https://github.com/tim99oth99e/circuit-to-latex) repo contains implementation of Deep Learning models that predicts the LaTeX code that corresponds to a given circuit diagram image. 

from images of electrical circuits.
