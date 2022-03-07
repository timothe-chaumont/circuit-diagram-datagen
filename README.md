# circuit-to-latex

Deep-learning model that predicts (CircuiTikz) LaTeX from images of electrical circuits.

## Steps to generate data (Windows)

- Install [LaTeX](https://www.latex-project.org/get/)
- Install [Ghostscript](https://ghostscript.com/releases/gsdnld.html)
- Create a file called _.env_ containing paths to `latex.exe` and `gswin64c.exe` binaries, in the same way as [_example.env_](/scripts/example.env) (put double quotes around dirnames that contain spaces).
