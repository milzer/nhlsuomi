# NHL Suomi

Generate a page of NHL scores, hilight videos and selected player stats based on country and name filters

### Prerequisites

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

Install packages:

```
pip install jinja2 praw pytest
```

Create config JSON (see [example.config.json](example.config.json)) and run the script:

```
python run.py -c config.json
```

## Running the tests

```
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
