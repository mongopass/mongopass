<div align="center">
    <img src=".repoassets/BannerApp.png" alt="MongoPass Banner">
</div>

# This is Mongo with Python app called MongoPass

## The MongoPass CLI app

![MongoPass Screenshot](.repoassets/screenshot.png)

## At Compass

![Alt text](.repoassets/screenshot_compass.png)

## First step, the .env

Please copy the `.env.example` file to `.env` and fill the variables with your own values.

```
cp .env.example .env
```

## To run the app

```
python -m venv venv
source ./venv/Scripts/activate
pip install pymongo bcrypt python-decouple
python ./do.py
deactivate
```

<div align="center">
    <img src=".repoassets/IconApp.png" alt="Mongo Pass">
</div>

## Pylar AI Creative ML Free License

This project is licensed under the [Pylar AI Creative ML Free License](LICENSE.md). For further details about this license, please visit the [official source HuggingFace/superdatas](https://huggingface.co/spaces/superdatas/free-license).
