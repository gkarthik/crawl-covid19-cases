## Crawl cases and save to file

## Dependencies

* [Scrapy](https://scrapy.org/)

## Configuration

1. Add config file (./covid19/config.py) to post ascii tables to URLs (Use case: Slack bot).

```
slack_sandiego_post_url = "<post-url>"
```

2. Create ./logs/ and ./data directories
3. Run command from base directory
```
scrapy crawl --logfile logs/$(date +%Y-%m-%d-%H-%M.log) -o data/items.csv sandiego
```

## Contribution

Pick a region and write a spider. I've tried to keep the classes TestingStats and CaseCategories as general as possible.
