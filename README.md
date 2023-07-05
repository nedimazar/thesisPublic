## Anonymized version of the repo for my MSc thesis: "Interfacing Operating Systems with Large Language Models"

## Dependencies
1. Python: `3.11.2`
2. `python3.11 -m venv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. Make sure `OPENAI_API_KEY` environment variable is set.

## `roger` (CLI agent):
### Installation
1. Alias the script in your `.bashrc`/`.zshrc` like this:
    * `alias roger="noglob [path_to_venv]/venv/bin/python [path_to_repo]/thesis/src/agent/roger.py"`
2. Also add the repository to your `PYTHONPATH`
    * `export PYTHONPATH=$PYTHONPATH:[path_to_repo]`

### Usage
* `roger [Natural Language Pompt]`

## `src/agent`
`roger`'s implementation lives here, you can edit the setup and fewshot promptsin `utils.py`.
Feel free to change `model="gpt-3.5-turbo"` to `model="gpt-4"` in `roger.py` to use GPT-4.

## `src/finetune`
The NL2Bash (Lin et al. 2018) dataset is used to fine-tune various GPT-3 models here. Data preparation, fine-tuning, and shell scripts to get predictions from the fine-tuned models can also be found here.

## `src/meta`
Contains an inference cost estimation script.

## `src/userStudy`
This directory contains the user study material. There are also scripts to annotate the experiments.
The `dockerStuff` directory was used to set up a container for participants to use in the second task of the user study.
