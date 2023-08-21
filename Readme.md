# This is Mongo with Python app called MongoPass

![MongoPass Screenshot](.repoassets/screenshot.png)

## First step, the .env

Please copy the `.env.example` file to `.env` and fill the variables with your own values.

```bash	
cp .env.example .env
```

## To run the app

```bash
python -m venv venv
source ./venv/Scripts/activate
pip install pymongo bcrypt python-decouple
python ./do.py
deactivate
```

## Pylar AI Creative ML Free License

This project is licensed under the [Pylar AI Creative ML Free License](LICENSE.md). For further details about this license, please visit the [official source HuggingFace/superdatas](https://huggingface.co/spaces/superdatas/free-license)