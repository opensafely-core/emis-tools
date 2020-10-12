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

First, you need to ssh into a VM that has production access. At the moment, there's only the test one:

    ssh <github_handle>@directorvm.testemisnightingale.co.uk

    # (unless you're seb in which case it's sebbacon)

Check you can access *director*:

    sebbacon@ip-10-0-3-179:~$ host directoraccess.emishealthinsights.co.uk
    directoraccess.emishealthinsights.co.uk has address 10.0.2.207
    directoraccess.emishealthinsights.co.uk has address 10.0.1.226
    directoraccess.emishealthinsights.co.uk has address 10.0.0.55

Ensure you have the latest docker image (with python + scripts packaged):

    docker pull docker.opensafely.org/emis-scripts

Run a command with the `TOKEN` and `USER` set in the environment.

For example, the `run_sql.py` command executes `acceptance-test-study.sql` with
all the views replaced with `_slice` suffixes, and writes a CSV to `/tmp`.

Build and push it with:

    cd scripts/
    ./build.sh

Then on the server, run it with:

    docker pull docker.opensafely.org/emis-scripts && time docker run --env TOKEN=1RmcPqwGN3yQp2SfDJ8v --env USER=sebastian.bacon -v $(pwd):/tmp docker.opensafely.org/emis-scripts python run_sql.py

