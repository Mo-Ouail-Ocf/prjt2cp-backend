# PRJP 2CP N06 BACKEND

## Get Started
Setup vertuel environment:
- on fedora38
	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
	```

- on windows (pls use linux)
	```sh
	python -m venv .venv
	Set-ExecutionPolicy RemoteSigned # run on Powershell as administrator in case of activate fail 
	.\.venv\Scripts\activate # for Cmd
	.\.venv\Scripts\Activate # for Powershell
	pip install -r requirements.txt
	```

Init the DB:
  ```bash
  python3 -m init
  ```

Run the web server:
```bash
uvicorn main:app --reload
```

Check the swagger docs:  `http://localhost:8000/docs`

NOTE: Use ruff for formatting
