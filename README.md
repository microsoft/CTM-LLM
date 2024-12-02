# Scaling Clinical Trial Matching Using Large Language Models: A Case Study in Oncology

[[Paper](https://arxiv.org/abs/2308.02180)] 


[Cliff Wong](https://scholar.google.com/citations?user=Sl05ifcAAAAJ&hl=en), [Sheng Zhang](https://scholar.google.com/citations?user=-LVEXQ8AAAAJ&hl=en), [Yu Gu](https://scholar.google.com/citations?user=1PoaURIAAAAJ&hl=en&oi=sra), [Christine Moung](https://www.semanticscholar.org/author/C.-Moung/7016395), [Jacob Abel](https://scholar.google.com/citations?user=xKOFq-MAAAAJ&hl=en&oi=sra), [Naoto Usuyama](https://www.microsoft.com/en-us/research/people/naotous/), [Roshanthi Weerasinghe](https://www.semanticscholar.org/author/R.-Weerasinghe/2131618433), [Brian Piening](https://scholar.google.com/citations?user=cpToe1oAAAAJ&hl=en&oi=ao), [Tristan Naumann](https://scholar.google.com/citations?user=cjlSeqwAAAAJ&hl=en), [Carlo Bifulco](https://scholar.google.com/citations?user=_um_DjQAAAAJ&hl=en&oi=ao), [Hoifung Poon](https://scholar.google.com/citations?user=yqqmVbkAAAAJ&hl=en)

## Release
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Contents
<!-- - [Data Download](#data-download) -->
- [Install](#install)
- [LLM extraction](#llm-extract)
- [Evaluation](#evaluation)

## Install

1. Clone this repository and navigate to CTM-LLM folder
```bash
git clone https://github.com/microsoft/CTM-LLM
cd CTM-LLM
```

2. Install Package: Create conda environment

```Shell
conda create -n ctm-llm python=3.10 -y
conda activate ctm-llm
pip install -r requirements.txt
```

## LLM Extract

Fill in your OpenAI API parameters in the file src/openai_api.py:
```Shell
openai.api_type = "azure"
openai.api_key = '...'
openai.api_base = 'https://example-endpoint.openai.azure.com/'
openai.api_version = "2023-03-15-preview"
DEPLOYMENT_ID="deployment-name"
```

## Evaluation

Below are several normalized LLM predictions files:
| LLM | path |
| :---: | :---: |
| GPT 3.5 0-shot |  predictions/gpt3p5_0shot.jsonl |
| GPT 4 0-shot |  predictions/gpt4_0shot.jsonl |
| GPT 4 3-shot |  predictions/gpt4_3shot.jsonl |
| Criteria2Query | predictions/criteria2query_entity_norm.jsonl |

To run evaluation, run the command below with the prediction file

```Shell
python evaluation/eval_gpt.py --input_pred_path <prediction file> --input_ground_truth_path labels/ground_truth_norm.jsonl
```

## Acknowledgement


If you find this work useful for your research and applications, please cite using this BibTeX:
```bibtex
@InProceedings{wong2023ctmllm,
      title={Scaling Clinical Trial Matching Using Large Language Models: A Case Study in Oncology}, 
      author={Wong, Cliff and Zhang, Sheng and Gu, Yu and Moung, Christine and Abel, Jacob and Usuyama, Naoto and Weerasinghe, Roshanthi and Piening, Brian and Naumann, Tristan and Bifulco, Carlo and Poon, Hoifung},
      booktitle={Proceedings of the 2nd Machine Learning for Health symposium},
      year={2023},
      volume={219},
      series={Proceedings of Machine Learning Research},
      publisher={PMLR},
      primaryClass={cs.CL},
      pdf={https://arxiv.org/pdf/2308.02180.pdf},
      url={https://arxiv.org/abs/2308.02180},
      abstract={Clinical trial matching is a key process in health delivery and discovery. In practice, it is plagued by overwhelming unstructured data and unscalable manual processing. In this paper, we conduct a systematic study on scaling clinical trial matching using large language models (LLMs), with oncology as the focus area. Our study is grounded in a clinical trial matching system currently in test deployment at a large U.S. health network. Initial findings are promising: out of box, cutting-edge LLMs, such as GPT-4, can already structure elaborate eligibility criteria of clinical trials and extract complex matching logic (e.g., nested AND/OR/NOT). While still far from perfect, LLMs substantially outperform prior strong baselines and may serve as a preliminary solution to help triage patient-trial candidates with humans in the loop. Our study also reveals a few significant growth areas for applying LLMs to end-to-end clinical trial matching, such as context limitation and accuracy, especially in structuring patient information from longitudinal medical records.}
}
```