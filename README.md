# Steam-to-calendar

View its Steam history on a calendar.

This program :

- Parse the Steam website and save the retrieved data to a file
- Generate an camera image based on a data file

The data retrieved is :

- [ ] The account creation date
- [ ] The achievements dates
- [ ] The purchases dates

## Run Locally

Clone the project

```bash
  git clone https://github.com/fsabre/steam-to-calendar.git
```

Go to the project directory

```bash
  cd steam-to-calendar
```

Install dependencies

```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
```

Run the program

```bash
  python stc.py
```
