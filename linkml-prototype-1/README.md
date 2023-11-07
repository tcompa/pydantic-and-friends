Trying to build a linkml model of ngff image from the ground up, since a first attempt via https://github.com/linkml/schema-automator failed.

How to:
```
python -m venv venv
source venv/bin/activate
pip install linkml

gen-pydantic ngff_image.yaml > ngff_image.py
```
