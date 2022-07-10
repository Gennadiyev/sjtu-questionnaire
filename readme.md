# SJTU Questionnaire

![requests>=2.6.0](https://img.shields.io/badge/requests-%3E%3D2.6.0-yellowgreen) ![python version support](https://img.shields.io/pypi/pyversions/requests)

[Chinese Simplied / 简体中文](readme_zh-cn.md)

A simple unofficial Python implementation of [SJTU Questionnaire API](https://wj.sjtu.edu.cn/). Supports multi-processing.

## Installation

```bash
pip install sjtu-questionnaire
```

## Quick Start

```python
import sjtuq as Q

# Create form object
form = Q.SJTUQuestionnaire("https://wj.sjtu.edu.cn/api/v1/public/export/83f581b4cfd3be8897bcabb23b25ef30/json")
# Get all answers
answers = form.get_all_data() # Get all data as a list

print("# Answers:", len(answers)) # 1. Only Kunologist have answered this questionnaire!
```

## Documentation

The documentation is generated using [`pydoctor`](https://github.com/twisted/pydoctor), hosted on [GitHub Pages](https://gennadiyev.github.io/sjtu-questionnaire/index.html) 

