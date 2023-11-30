> [!WARNING]  
> This code is no longer usable due to nhl.com closing the old API and the new API doesn't provide player nationalities, which were the whole point here. While the filtering could be done based on names only, I find it too cumbersome to maintain. Thus archiving the project.

# NHL Suomi

Generate a page of NHL scores, hilight videos and selected player stats based on country and name filters

### Requirements

* Python 3.8

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

## NHL API

https://gitlab.com/dword4/nhlapi

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
