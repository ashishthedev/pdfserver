# Pdfserver


## Installation

### Installing Wkhtmltopdf
The project is using static binaries available at http://wkhtmltopdf.org/downloads.html
Please download the appropriate binary as per your operating system and copy in the bin folder.

### Virtual environment
Create virtual env for the pdfserver using virtualenvwrapper or virtualenv. Both are capable enough to carry the task but virtualenvwrapper is superior and is a natural evolution of the latter. 

If you are not aware of the tool, please go through a tutorial(http://code.tutsplus.com/articles/python-power-tools-virtualenvwrapper--net-31569)

The official documentation can be found at: http://virtualenvwrapper.readthedocs.io/en/latest/ 

#### Activate the virtualenv
```
workon pdfserver
```

### Installing dependencies with pip

```
pip install -r requirements.txt
```

### Run the local server
Please make sure you are inside the activated virtualenv. Once confirmed, please run:
```
python run.py
```

### Verify
Verify the setup by visiting http://localhost:8181/
