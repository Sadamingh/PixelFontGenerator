# PixelFontGenerator

- JP fonts from https://osdn.net/downloads/users/8/8541/jfdotfont-20150527.7z/
- EN fonts from https://www.dafont.com/bitmap.php
- Text Corpus from https://alaginrc.nict.go.jp/WikiCorpus/index_E.html



### How to use?

* Put the background files in `raw_bg`.
* Run the clipper file.

```
python clipper.py
```

* Run the generator file. The first argument should be how many pictures you want to generate for each language `en/jp`. The second argument should be the madximum number of text you want to generate in one picture.

```
python generator.py 20000 10
```
