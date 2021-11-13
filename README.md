# The recommended way of installing

    python3 -m venv venv # recomended python 3.6
    .\env\Scripts\activate
    pip install -e .
    pip install --upgrade pip
    pip install -r requirements.txt
    # Your settings here:
    export SPIRAL_DATABASE_ENGINE=

# Updating requirements.txt

requirements.txt stores the dependency versions used during the development. During deployment, the same versions are installed to preserve reproductivity. 
The `pip freeze` command above should be repeated after updating dependencies in order to update requirements.txt.
