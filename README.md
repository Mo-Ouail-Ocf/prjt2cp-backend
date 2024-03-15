# PRJP 2CP N06 BACKEND

## Get Started
Setup vertuel environment:
- on fedora38
	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
	```

-	on windows (pls use linux)
	```sh
	python -m venv .venv
	Set-ExecutionPolicy RemoteSigned # in case of activate fail (run on Powershell as administrator)
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
uvicorn app:main --reload
```

Check the swagger docs:  `http://localhost:8000/docs`

NOTE: Use ruff for formatting
