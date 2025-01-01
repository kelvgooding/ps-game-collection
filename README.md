# PSN Game Collection

A script which gathers data based on your collection on PlayStation 4 and PlayStation 5 games directly from your PSN account.

## Reqrequisisit

psn_token sso cookie can be obtained by first login into your PSN account https://www.playstation.com/en-gb/ and use the following link to find the npsso value: https://ca.account.sony.com/api/v1/ssocookie. Add this value into auth.py on Line 6

## Steps:

1. Clone the repository

2. Navigate to the directory and install the required modules:

```
pip install --break-system-packages -r requirements.txt
```

3. Run the following python script:

```
python3 psn_data.py
```

4. This will export 2 files:

* psn_game_collection.db
* psn_game_collection.csv
