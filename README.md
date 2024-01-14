# invest-track

## Run application locally (without docker)

To create the local environment:

````shell
pyenv local && pyenv install
virtualenv --python=`pyenv which python` venv
source venv/bin/activate
pip install pip setuptools --upgrade
pip install -r ./Django/requirements.txt
````