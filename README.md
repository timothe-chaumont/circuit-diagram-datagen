# Circuit Diagram Datagen

Codebase for electric circuit diagram data generation, to train machine learning models.

Each generated example is composed of:
- The [CircuiTikz](https://ctan.org/pkg/circuitikz) (LaTeX) code that describe the diagram,
- The compiled image for that code.

![Example of one generated circuit](/generated_data_example.png)
_Example of a generated circuit diagram._

## Steps to generate data (Windows)

1. Install the dependencies with `make install`
2. Install [LaTeX](https://www.latex-project.org/get/)
3. Install [Ghostscript](https://ghostscript.com/releases/gsdnld.html)
4. Create a file called _.env_ containing paths to `latex.exe` and `gswin64c.exe` binaries, in the same way as [_example.env_](/example.env).
5. Run `make generate` in a cmd window from the root directory

---
The [circuit-to-latex](https://github.com/timothe-chaumont/circuit-to-latex) repo contains implementations of Deep Learning models that predict the LaTeX code for a given circuit diagram image. 
