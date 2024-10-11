# sql-olympics-server
Web app that connects to MySQL database to display pre-defined queries, procedures and views via SQL and python

## How to use
1. Clone the repo
2. `cd sql`
3. Create a mySQL user with the name 'dsuser' and password 'userCreateSQL' (if not already)
4. run `mysql --local_infile=1 -u dsuser -p`
5. Enter password (userCreateSQL)
6. Run `\. init_database.sql` - this will fill databases with everything required
7. Run the following commands:
```
cd ..
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app
python3 app.py

```
8. Have fun!

