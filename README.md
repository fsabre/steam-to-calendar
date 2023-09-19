# Steam-to-calendar

View its Steam history on a calendar.

This program :

- Parse the Steam website and save the retrieved data to a file
- Generate an calendar image based on a data file

The data retrieved is :

- [ ] The account creation date
- [X] The achievements dates
- [ ] The purchases date

## FAQ

### Why don't you use the official Steam API ?

- No way to fetch data from private profiles
- No way to fetch purchase date

### Can this program fetch data from private profiles ?

Yes, you can ! Use the `--login` flag to be redirected on the Steam login page when the program starts. Once you are
logged in, you'll be able to parse data from yourself and from your friends if they allowed you to do so.

## Run locally

Clone the project and go to the directory :

```bash
  git clone https://github.com/fsabre/steam-to-calendar.git
  cd steam-to-calendar
```

Install the dependencies in a virtual environment :

```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
```

Install the Playwright browser :

```bash
  playwright install chromium
```

## Usage

Start to fetch your data with the `fetch` command, then draw the calendar with `draw` :

```bash
  python stc.py fetch YOUR_STEAM_PROFILE_URL  # Add --login if your profile is private
  python stc.py draw
```

Additional help for the command line options is available with :

```bash
  python stc.py fetch --help
  python stc.py draw --help
```

## Screenshots

### HTML export

![Example of HTML export](./img/html-export-example.png "Example of HTML export")

### Text export

```text
----- 02/2022 -----     1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28                       
Crypt of the Nec        X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   X   X   .   .   .   .   .   .   .   X   X                        
Dying Light             .   .   .   .   .   X   X   X   X   X   .   .   .   X   .   .   .   .   X   X   X   .   .   .   .   .   .   .                        
Halo Infinite           X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .                        
Paladins                .   .   .   .   X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .                        
Phoenix Wright:         .   X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .                        
----- 03/2022 -----     1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31           
BioShock Infinit        .   .   .   .   .   .   .   .   .   .   .   .   .   X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .            
Crypt of the Nec        .   .   X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .            
Dying Light             .   .   .   .   .   .   .   X   X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .            
Omensight               .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   X   X   X   .   X   .   .   .   .   .   .   .   .            
----- 04/2022 -----                 1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30   
Crypt of the Nec                    .   .   .   .   .   .   .   .   .   X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .    
Dying Light                         .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   X   X   .   .   .   .   .   .   .   .   .   .   .   .   .    
Omensight                           .   X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .    
----- 05/2022 -----                         1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31                   
Aim Lab                                     .   .   .   .   .   .   .   .   .   X   X   .   X   .   .   .   .   .   .   .   .   .   .   X   .   .   X   .   .   .   .                    
Eastshade                                   .   .   .   .   .   .   .   .   .   .   X   .   X   .   X   .   .   .   .   .   X   .   .   .   .   .   .   X   .   .   X                    
----- 06/2022 -----         1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30           
Little Nightmare            .   .   X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   X   .   .   .   X   .   .   .   .   .   .   .            
Phoenix Wright:             .   .   .   X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .            
Phoenotopia Awak            .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   X            
----- 07/2022 -----                 1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31
Phoenotopia Awak                    .   X   X   .   X   .   .   .   X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   X   .   .   .
----- 08/2022 ----- 1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31               
Phoenotopia Awak    .   X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   X   .   X   .   .   .   .   X   X   X   .                
----- 09/2022 -----             1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30       
ANNO: Mutationem                .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   X   X   X   .   X   X        
GRIS                            .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   X   X   X   .   X   X   .   .   .   .   .   .   .        
Knockout City™                  .   .   .   .   .   .   .   .   .   .   X   .   .   .   X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .        
----- 10/2022 -----                     1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31                       
ANNO: Mutationem                        X   X   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .          
```
