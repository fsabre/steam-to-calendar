# Steam-to-calendar

View its Steam history on a calendar.

This program :

- Parse the Steam website and save the retrieved data to a file
- Generate an calendar image based on a data file

The data retrieved is :

- [ ] The account creation date
- [X] The achievements dates
- [ ] The purchases date

## Run Locally

Clone the project and go to the directory

```bash
  git clone https://github.com/fsabre/steam-to-calendar.git
  cd steam-to-calendar
```

Place the webdriver corresponding to your web
browser ([Selenium documentation](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/))
in the directory (works with Chromium-based browsers for now)

Update the paths in `src/config.py`

```python3
CHROME_PATH: Final = r"C:\Program Files\Vivaldi\Application\Vivaldi.exe"
CHROME_DRIVER_PATH: Final = "chromedriver.exe"
```

Install dependencies

```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
```

Run the program

```bash
  python stc.py fetch YOUR_STEAM_PROFILE_URL
  python stc.py draw
```
