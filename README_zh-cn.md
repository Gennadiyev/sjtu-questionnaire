# SJTU 问卷服务 Python API（非官方）

![requests>=2.6.0](https://img.shields.io/badge/requests-%3E%3D2.6.0-yellowgreen) ![python version support](https://img.shields.io/pypi/pyversions/requests)

非官方的 [上海交通大学智能问卷服务](https://wj.sjtu.edu.cn/) 的 Python API，支持多线程。

## 安装

```bash
pip install sjtu-questionnaire
```

## 快速上手

```python
import sjtuq as Q

# 创建问卷对象
form = Q.SJTUQuestionnaire("https://wj.sjtu.edu.cn/api/v1/public/export/83f581b4cfd3be8897bcabb23b25ef30/json")
# 获取所有答案，拒绝分页，从我做起
answers = form.get_all_data()

print("# Answers:", len(answers)) # 返回答卷列表
```

## Documentation

The documentation is generated using [`pydoctor`](https://github.com/twisted/pydoctor), hosted on [GitHub Pages](https://gennadiyev.github.io/sjtu-questionnaire/index.html) 

