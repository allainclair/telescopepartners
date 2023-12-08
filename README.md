## [Pyenv](https://github.com/pyenv/pyenv)

Setup [Pyenv](https://github.com/pyenv/pyenv), if you will, or use Python 3.12.0 for this project

## [PDM](https://pdm-project.org)
It is a package manager for Python projects. It is similar to poetry or pipenv.
### Install [PDM](https://pdm-project.org)

```bash 
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
```

### Install dependencies of this project
```bash
pdm install
```

### Install browser binaries for Chromium, Firefox, and WebKit
```bash
pdm run playwright install
```

## Config (src/config.py)

* `src/config.py` has an **email** and **password** created to access LinkedIn.
Feel free to use it. You can change it to your own account.

* CSV files are pointed by:
  * `COMPANY_NAMES_PATH` input of **only** company names. Change it to test other companies.
  * `COMPANY_NAME_URLS_EMPLOYEES_PATH` output created of companies' URL and number of employees
    with the header `company,url,employees`. It will be created after `pdm run python main`.
* `SLEEP_TIME_FOR_LOGIN` is the time to wait for the user to log into LinkedIn. 
  IMPORTANT: You may need to do it manually because of the captcha and security check.

## Run project

```bash
pdm run main
```

## Future improvements

* Add more companies for test cases.
* Try to bypass the captcha and security check.
* Try to parallelize the process, e.g., using asyncio.gather,
  It didn't work on the first try.
