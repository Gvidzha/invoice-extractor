# NER OCR Projekts

Šis projekts apvieno Named Entity Recognition (NER) ar optisko rakstzīmju atpazīšanu (OCR), lai analizētu dokumentus.

## Struktūra

- `src/`: galvenais avots ar apakšmoduļiem (`ocr`, `ner`, `preprocessing` utt.)
- `notebooks/`: Jupyter piezīmju grāmatas modeļu testēšanai un analīzei
- `configs/`: konfigurācijas faili
- `data/`, `results/`: dati un rezultāti (nav iekļauti Git repozitorijā)

## Palaišana Colab

👉 [Atvērt Google Colab](https://colab.research.google.com/github/<lietotājvārds>/<repo-nosaukums>/blob/main/notebooks/<fails>.ipynb)

## Uzstādīšana lokāli

```bash
conda env create -f environment.yml
conda activate ner_ocr_env
