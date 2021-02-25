A scratchpad for notes, some of which could make it to structured documentation, later

# Accessing production EMISX via browser ("Visualiser")

## Register

* Visit https://www.emishealthinsights.co.uk/, register with `firstname.lastname`
* Set up 2FA
* Go to SQL Lab and test:

```sql
SELECT * from hive."extract_oxford_datalabs".patient_slice
limit 100
```

You can examine table schemas using a dropdown on the left-hand side.

# Accessing production EMISX from command line

You will want to hop via a jumphost - currently by adding this to your `.ssh/config`:

```
Host emis
  HostName directorvm.testemisnightingale.co.uk
  ProxyJump web2.openprescribing.net
  ForwardAgent yes
```

Now you can ssh into a VM that has production access. At the moment, there's only the test one:

    ssh <github_handle>@emis
    
    # (unless you're seb in which case it's sebbacon)


Check you can access *director*:

    sebbacon@ip-10-0-3-179:~$ host directoraccess.emishealthinsights.co.uk
    directoraccess.emishealthinsights.co.uk has address 10.0.2.207
    directoraccess.emishealthinsights.co.uk has address 10.0.1.226
    directoraccess.emishealthinsights.co.uk has address 10.0.0.55
    
Ensure you have [certificates set up](https://team-manual.thedatalab.org/tech_team_playbooks/accessing-emis-data/)

To run a query you have to provide a path to a certificate, a certificate password, and a username in your environment:

```
USER=<user_that_you_login_to_emis_web_with>
PFX_PATH=<path_to_cert_file>
PFX_PASSWORD_PATH=<path_to_cert_password_file>
```

You can then run the scripts from this repo.  The `run_sql.py` script takes a sql file whose contents should be executed as the first argument and a path to a CSV file to where results should be written as the second argument.  A minimal SQL that just tests the connection is provided at `sql/test.sql` and can be run like this:


```py
python run_sql.py sql/test.sql output_file.csv 


