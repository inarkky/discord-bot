# Discord chatbot

All modules are sourced from `cog/` except for the chatbot functionality which is defined inside `on_message` event in `bot.py`

NOTE: with the dataset, the size of dependencies is somewhere north of 2GB so if you are low on bandwidth I suggest you comment following 3 lines in `bot.py` (to skip downloading the datasets). Chat functionality won't function without those, but you will save money.

```python
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
ranker = AutoModelForSequenceClassification.from_pretrained('microsoft/DialogRPT-human-vs-machine')
```
Alernatively, you can forego pretrained models and feed her your own, just be warned that it's very resource intensive.

## Installation
> Tested on python version 3.9  

```bash
$ pip install -r requirements.txt 
$ python bot.py  
```

Also, there is possibility that i forgot to add some dependencies in requirements.txt, but python's debugger should warn if that's the case
