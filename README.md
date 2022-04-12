# circuit-to-latex

Deep-learning model that predicts [CircuiTikz](https://ctan.org/pkg/circuitikz) (LaTeX) from images of electrical circuits.

## Steps to generate data (Windows)

1. (Create a virtual environment and) install the dependencies with `make install`
2. Install [LaTeX](https://www.latex-project.org/get/)
3. Install [Ghostscript](https://ghostscript.com/releases/gsdnld.html)
4. Create a file called _.env_ containing paths to `latex.exe` and `gswin64c.exe` binaries, in the same way as [_example.env_](/example.env).
5. Run `make generate` in a cmd window from the root directory

## To start the training 
1. (Create a virtual environment and) install the dependencies with `make install`
2. Run `make train` in a cmd window from the root directory