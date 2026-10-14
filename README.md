# End-to-End CI/CD Pipeline Automation

Learning project: GitHub → automated tests → Docker image → Jenkins local demo deployment → HTTP health check. GitHub Actions also runs tests and builds the image on pushes and pull requests.

## Prerequisites
- Git
- Python 3.11+
- Docker Desktop (Windows) or Docker Engine (Linux)
- Optional Jenkins agent with Git, Python and Docker installed and available to the Jenkins service account

## 1. Run locally on Windows PowerShell
From this project folder:
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -v
.\.\.venv\Scripts\python.exe app.py
```
If the last command path above is mistyped by your shell, use this exact command:
```powershell
.\.venv\Scripts\python.exe app.py
```
Open http://127.0.0.1:5000 and http://127.0.0.1:5000/health. Stop with Ctrl+C.

## 2. Run locally on Linux/Ubuntu/macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pytest -v
python app.py
```

## 3. Run with Docker
Ensure Docker Desktop/Engine is running:
```bash
docker build -t end-to-end-cicd-demo:1.0 .
docker run -d --name end-to-end-cicd-demo -p 5000:5000 end-to-end-cicd-demo:1.0
```
Open http://localhost:5000 and http://localhost:5000/health.
```bash
docker ps
docker logs end-to-end-cicd-demo
docker stop end-to-end-cicd-demo
docker rm end-to-end-cicd-demo
```
If port 5000 is occupied, map `-p 5001:5000` and open http://localhost:5001. If the container name already exists, run `docker rm -f end-to-end-cicd-demo` before starting again.

## 4. Push to GitHub
Create an empty repository on GitHub, then run in this project directory:
```bash
git init
git add .
git commit -m "Add end-to-end CI/CD demo"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```
Replace the URL with your real repository URL. GitHub Actions will run automatically on pushes and pull requests to `main`.

## 5. Configure Jenkins (optional)
1. Install Jenkins and ensure the agent can run Git, Python, and Docker.
2. Create a Pipeline job.
3. Under Pipeline, choose **Pipeline script from SCM**, select Git, enter your repository URL, set branch to `*/main`, and script path to `Jenkinsfile`.
4. Save, select **Build Now**, and inspect **Console Output**.
5. If successful, open http://localhost:5000 on the same machine as the Docker host.

Troubleshooting:
- Docker command/daemon error: start Docker and ensure the Jenkins service account has permission to use it.
- Git not found: install Git on the agent and configure Jenkins tool settings.
- Python not found: install Python and ensure the Jenkins service account can find it.
- Port conflict: stop/remove the existing demo container or change `APP_PORT` in the Jenkinsfile.
- Failed tests: inspect the first failing stage; the pipeline should stop before deployment.

## Workflow
1. Developer pushes code to GitHub.
2. GitHub Actions runs tests and builds an image; Jenkins can run the separate Jenkins pipeline.
3. Pytest validates the home and health endpoints.
4. Docker creates a versioned image.
5. Jenkins replaces the old local demo container and starts the new version.
6. A health request checks that the deployed app responds.

## Resume description (only after implementing and testing)
**End-to-End CI/CD Pipeline Automation | Python, Flask, Git, GitHub Actions, Jenkins, Docker, Linux**
- Built a CI workflow to run automated Pytest checks on GitHub pushes and pull requests.
- Created a Docker image for a Flask application and configured Jenkins stages for testing, image building, local deployment, and HTTP health verification.
- Practised troubleshooting test failures, container startup errors, and port conflicts using pipeline logs and Docker commands.

Only list Jenkins if you actually ran the Jenkins pipeline. If you only ran GitHub Actions, mention GitHub Actions and Docker. Do not claim public cloud or production deployment unless you implement and verify it.
