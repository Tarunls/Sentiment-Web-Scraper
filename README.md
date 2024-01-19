# SentiScrape

SentiScrape is a BS4 and Selenium powered web scraper that scrapes websites for data, and then directly compares that data to
a sentiment analysis model (Bert).

For now the main focus of this scraper is on IMDB Reviews and is also utilizing the OpenMovieDB API

## Dependencies

To run this python script install the following libraries:

```bash
pip install torch torchvision torchaudio requests transformers bs4 pathlib pandas matplotlib seaborn
```

## Usage

In order to choose a movie to run the scraper for change the movie name in

```python
moviename = 'avengers_endgame'
```
The default movie is already set to end game. Spaces should be replaced with '_'

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

Contributors can be found in the contributor section

## License

[MIT](https://choosealicense.com/licenses/mit/)