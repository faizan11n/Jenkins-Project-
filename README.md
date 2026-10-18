# Jenkins Projects

Hands-on Jenkins practice: Jenkins running in Docker on an AWS EC2 instance, built step by step.

| # | Project                        | What it demonstrates                                                |
|---|---------|----------------------|
| 1 | Freestyle job `hello-jenkins`  | Install Jenkins, create a Freestyle job, run `echo "Hello Jenkins"` |
| 2 | `project2-python-pipeline/`    | Declarative Pipeline from SCM: `Checkout -> Run Script -> Archive Result` for a Python script, with `archiveArtifacts` |
| 3 | `project3-env-post/`           | `environment` block (repo URL and variables) and `post { success / failure / always }` |
| 4 | GitHub webhook                 | Push to GitHub automatically triggers the Jenkins build (real-time CI) |

## Repository layout
```
jenkins/docker-compose.yaml        # Jenkins LTS (JDK 17) in Docker, port 8099
project2-python-pipeline/          # hello.py + Jenkinsfile
project3-env-post/                 # Jenkinsfile with environment + post blocks
```

## Run Jenkins
```bash
cd jenkins
docker compose up -d
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword   # first login
# open http://<EC2-IP>:8099
```
Python is needed inside the container for project 2:
```bash
docker exec -u root jenkins apt-get update && docker exec -u root jenkins apt-get install -y python3
```

## Pipeline job settings (projects 2 and 3)
- Definition: Pipeline script from SCM, SCM: Git
- Branch: `*/main`
- Script Path: `project2-python-pipeline/Jenkinsfile` or `project3-env-post/Jenkinsfile`

## Webhook (project 4)
1. Job, Configure, Triggers: tick **GitHub hook trigger for GITScm polling**
2. GitHub repo, Settings, Webhooks: payload URL `http://<EC2-IP>:8099/github-webhook/`, content type `application/json`, push event
3. Open inbound port 8099 in the EC2 Security Group

## Problems solved along the way
- `Unable to find Jenkinsfile`: file was committed as `jenkinsfile`; Linux paths are case-sensitive, fixed with `git mv`
- Nested git repo (`does not have a commit checked out`): removed the inner clone
- Webhook `failed to connect to host`: EC2 public IP had changed after stop/start; updated the payload URL
- Locked-out Jenkins: recreated the container with a fresh volume

## Notes
- EC2 public IP changes after stop/start. An Elastic IP avoids breaking the webhook
- Keep port 8099 restricted to your own IP when not testing webhooks
