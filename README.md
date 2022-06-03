# NHL Suomi

Generate a page of NHL scores, hilight videos and selected player stats based on country and name filters

### Requirements

* Python 3.7
* jinja2
* praw

### Installing

Using virtualenv is highly recommended:

```
python3 -m venv .env
source .env/bin/activate
pip install --upgrade pip
```

Install required packages:

```
pip install -r requirements.txt
```

Create config JSON (see [example.config.json](example.config.json)) and run the script:

```
python run.py -c config.json
```

## Running the tests

```
pytest
```

## NHL API

https://gitlab.com/dword4/nhlapi

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
