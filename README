# No name tool for mass uploading foreign curencies exchange rates to all businesses in manager.io
[manager.io](https://manager.io) is the easy to use, extensible ERP system with web interface and powerful API, that can suite requirements of many companies.

Currently (2023-02-13), unfortunately, the system does not provide functionality for setting exchange rates for ALL businesses at a time, since currencies and exchange rates of different companies are separate objects from separate databases.
Also, the developers do not have it on the roadmap.

So, there is where my application could help you.

# Installation

As simple as possible. Just clone the repo, install `python3-tk` and make `main.py` executable.

# Usage

The UI and template are in Polish. I'm a very lazy person, so translate it if you like. I'm not a Pole, just the users are Poles, it's for that reason.

So, if you'd like to try the application:

1. Launch the `main.py` being in the directory it's located.
2. Click "Pobierz szablon" to download the template
This action downloads the foreign businesses and information about currencies they're using. Then generates a `.csv` table with that information.
3. Click "Otwórz szablon".
This action opens generated `.csv` template and if open/libre/another office suite application for editing spreadsheets is set to be default system-wide, it will be used. 
A bit on the template: "Data" is for *date*, it's the date for the day these exchange rates were applicable. Set it in a ISO format, e. g. YYYY-MM-DD
"Waluta_bazowa" is for *base currency*. Under that line are located the currencies for businesses, which have this currency set as a base one. For example, you see base currency `USD`. Under that line, you see `EUR`. The cell  in the next to `EUR` column represents `EUR/USD` exchange rate at the date set in the first line of the template.
Numbers can be specified with both separators, `.` or `,`. Btw, only 4 digits after separator are saved, other will be ignored.
DO NOT TOUCH the value "Ilość kursów". This stands for "number of exchange rates" and helps the program to understand how many exchange rates are located under the base currency line.
Btw2. You are not obligated to set ALL of the exchange rates, only required ones. The program ignores empty cells in the template.
4. After you done editing the template, click "Ustaw kursy walut" (Set exchange rates) and wait for the process to end.
5. IF YOU ADDED/REMOVED A BUSINESS OR A FOREIGN CURRENCY, CLICK THE BUTTON "Wyczyść pamięć podręczną" (Clear cache) BEFORE PERFORMING ANY OTHER OPERATIONS.
6. For the maintaining purpose, there is a logging mechanism. By defalt, the log is saved to `./log/` directory to file `operational.log`. The log is quite descriptive, so if you've got into some trouble, try reading.

# Requirements

Code is not very linux-bound (or POSIX), so, if you try to run on Windows, do not forget to edit the code and replace all path separators to "backslash" `\` character.
There is no other platform binds in code, as I remember. So, the main requirements are:
- Python (~3.6+)
- Tk interface for Python (on debian-based linux distros called `python3-tk`)

 
