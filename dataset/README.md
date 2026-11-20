# Cybersecurity Knowledge and Skills Taught in Capture the Flag Challenges

This repository contains supplementary materials for the following journal paper:

Valdemar Svabensky, Pavel Celeda, Jan Vykopal, and Silvia Brisakova.
Cybersecurity Knowledge and Skills Taught in Capture the Flag Challenges.
In Elsevier Computers & Security. 2020.

## Contents

We now describe the directory structure and the individual files. Please note that we were 
not allowed to publish all files because of copyright (see Section 6.3 of the paper).

* `data`: a folder with an incomplete sample of the `keywords.json` file with the cybersecurity 
keywords extracted from the [CSEC2017 curricula](https://cybered.hosting.acm.org/wp/), along with 
its JSON schema (`schema.json`) for validation. We were unable to publish the full `keywords.json`.
* `data_urls_only/writeups`: a folder structure of files with URL links to the analyzed writeups. 
For the analysis, a folder `data/writeups` with the contents of the actual writeups is required. 
However, we were unable to publish the contents of `data/writeups`.
* `figures`: a folder with two PDFs: a graph of CTF event counts (`ctf-counts.pdf`) and the 
paper's graphical abstract (`graphical-abstract.pdf`), along with their LaTeX source files and a 
list of Knowledge Units not found in any of the writeups (`missing-knowledge-units.txt`).
* `src/writeup_analyzer.py`: a Python script for analyzing the writeups' contents with the help 
of [CSEC2017 curricula](https://cybered.hosting.acm.org/wp/).
* `src/writeup_downloader.py`: a placeholder file with pseudocode for downloading the writeups' 
contents from [CTFtime.org](https://ctftime.org/). We were unable to publish the full code.
* `LICENSE`: a file with the MIT license used for the source code.
* `README.md`: this file.
* `requirements.txt`: a file that specifies the Python modules required for running the code.

## General requirements

Running the code requires Python 3.7 or higher and the modules from the `requirements.txt` file.

Download Python from [python.org](https://www.python.org/downloads/) and install it.
Then, install all requirements with 
```bash
pip install -r requirements.txt
```
## Description of `writeup_analyzer.py`

This file analyzes the downloaded writeups. For more information, see Section 4.3 of the paper.

**Input**: The script takes one optional command-line argument specifying the path to the analyzed 
writeups. The path must exist. If no path is given, writeups in the default path `../data` are 
analyzed. Additionally, the script needs a `keyword.json` file as an input in the same folder as 
the data, that is, `../data/keywords.json` by default.

**Usage**: The file can be executed as follows.
```bash
python writeup_analyzer.py [path_to_writeups]
```
However, it currently raises an exception because the writeup data and keywords are incomplete.
If you download the writeups and extend the `keywords.json` file, the analysis will work as intended.

**Output**: The results of the analysis (Section 5 of the paper). Since the script requires 8 KAs 
and 55 KUs in the `keywords.json` file, the usage of the attached incomplete `keywords.json` file 
raises an exception.

The code was tested on Windows 10.
