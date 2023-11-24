# NEO Readme

## Development Setup

### Prerequisites
Python 3.x
pip

### Setup
We use virtualenv for our environment.
* [Virtual Environments Guide](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments)

```commmandline
# Clone the repository if not already done. 
git clone https://github.com/harshith47/DBMS-Group20-BE.git

# Create a virtualenv
python -m venv .venv

# Activate the environment
.venv\Scripts\Activate #on windows, Try source command for linux or check guide linked above.

# Install requirements
pip install -r requirements.txt
```

### Running the app
```commandline
# Environment Variables
There's a .env file in the neo directory. Update your credentials like database username and password in the file.

# Flask Run
flask --app neo run --debug
```
 


