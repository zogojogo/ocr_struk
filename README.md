# OCR STRUK

**Created during an internship at nodeflux**

# How to run

clone this repository:
```bash
git clone https://github.com/Deanazor/ocr_struk.git
```

Go to repository folder :

```bash
  cd ocr_struk
```

I recommend to create a virtual environment first. After that, init environment:
```bash
  sh InitApp.sh
```

Run inference:
```python
python inference.py --image_path="your/image/path"
```

Draw result:
```python
python draw.py --img_path="your/image/path"
```