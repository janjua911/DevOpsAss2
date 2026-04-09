# Assignment-2 Complete Guide
## Hassan Janjua's Task Board — DevOps for Cloud Computing
**COMSATS University, Islamabad | Spring 2026**

---

## 📁 Project Structure

```
hassan-taskboard/
├── app.py                      # Flask web application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image build instructions
├── docker-compose.yml          # Part I: production deployment
├── docker-compose-jenkins.yml  # Part II: Jenkins CI/CD deployment
├── Jenkinsfile                 # Jenkins pipeline script
├── .gitignore
└── templates/
    └── index.html              # Frontend UI
```

---

## ✅ PRE-REQUISITES (on your EC2 instance)

SSH into your EC2 instance, then run:

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu   # allow running docker without sudo
newgrp docker

# Install Docker Compose plugin
sudo apt install -y docker-compose-plugin
docker compose version           # verify

# Install Git
sudo apt install -y git
```

> **Security Group:** Make sure your EC2 Security Group inbound rules allow:
> - Port 22 (SSH)
> - Port 5000 (Part I app)
> - Port 5001 (Part II Jenkins app)
> - Port 8080 (Jenkins UI)

---

## 🐙 GITHUB SETUP

```bash
# On your LOCAL machine (or EC2), push the project to GitHub
git init
git add .
git commit -m "Initial commit: Hassan Janjua Task Board"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/hassan-taskboard.git
git push -u origin main
```

---

## PART I — Containerized Deployment on AWS EC2

### Step 1 — Push image to Docker Hub

```bash
# Login to Docker Hub
docker login

# Build the image
docker build -t hassanjanjua/taskboard:latest .

# Push it to Docker Hub
docker push hassanjanjua/taskboard:latest
```

### Step 2 — Clone project on EC2

```bash
git clone https://github.com/YOUR_USERNAME/hassan-taskboard.git
cd hassan-taskboard
```

### Step 3 — Launch the app

```bash
docker compose up -d
```

This will:
- Pull the `hassanjanjua/taskboard:latest` image (or build locally)
- Start the MySQL container with a **persistent named volume** (`db_data`)
- Start the Flask web app container
- Connect them over an internal bridge network

### Step 4 — Verify it's running

```bash
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE                           PORTS                    NAMES
xxxx           hassanjanjua/taskboard:latest   0.0.0.0:5000->5000/tcp   hassan_taskboard_web
xxxx           mysql:8.0                       0.0.0.0:3306->3306/tcp   hassan_taskboard_db
```

### Step 5 — Open in browser

```
http://<YOUR-EC2-PUBLIC-IP>:5000
```

You should see **Hassan Janjua's Task Board** 🎉

### Step 6 — Test persistence

1. Add a few tasks in the UI
2. Run `docker compose down`
3. Run `docker compose up -d` again
4. Tasks should still be there (data survived because of the volume)

---

## PART II — Jenkins CI/CD Pipeline on AWS EC2

### Step 1 — Install Jenkins on EC2

```bash
# Install Java (Jenkins requirement)
sudo apt install -y openjdk-17-jdk

# Add Jenkins repository
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | \
  sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install -y jenkins

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Give Jenkins access to Docker
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Step 2 — Access Jenkins UI

Open: `http://<EC2-PUBLIC-IP>:8080`

Get initial admin password:
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

- Install **suggested plugins**
- Create your admin user

### Step 3 — Install required plugins

Go to: **Manage Jenkins → Plugins → Available**

Install:
- ✅ Git Plugin
- ✅ Pipeline Plugin
- ✅ Docker Pipeline Plugin

Restart Jenkins after installing.

### Step 4 — Add Docker Hub credentials to Jenkins

Go to: **Manage Jenkins → Credentials → Global → Add Credentials**

- Kind: Username with password
- Username: `hassanjanjua` (your Docker Hub username)
- Password: your Docker Hub password
- ID: `dockerhub-credentials`  ← must match the Jenkinsfile exactly

### Step 5 — Create Jenkins Pipeline

1. Click **New Item** → Enter name: `hassan-taskboard` → Select **Pipeline** → OK
2. Scroll to **Pipeline** section
3. Select **Pipeline script from SCM**
4. SCM: **Git**
5. Repository URL: `https://github.com/YOUR_USERNAME/hassan-taskboard.git`
6. Branch: `*/main`
7. Script Path: `Jenkinsfile`
8. Save

### Step 6 — Configure GitHub Webhook

On GitHub → Your repo → **Settings → Webhooks → Add webhook**

- Payload URL: `http://<EC2-PUBLIC-IP>:8080/github-webhook/`
- Content type: `application/json`
- Trigger: **Just the push event**
- Active: ✅

In Jenkins pipeline settings: enable **GitHub hook trigger for GITScm polling**

### Step 7 — Test the pipeline

Push any small change to GitHub:
```bash
echo "# trigger" >> README.md
git add . && git commit -m "Trigger Jenkins pipeline"
git push
```

Jenkins should automatically trigger, and you'll see all stages running.

### Step 8 — Verify Part II deployment

```bash
docker ps
```

You should see `hassan_jenkins_web` on port **5001** and `hassan_jenkins_db` on **3307**.

Open: `http://<EC2-PUBLIC-IP>:5001`

---

## 📸 SCREENSHOTS TO INCLUDE IN REPORT

### Part I
- [ ] `docker build` output
- [ ] `docker push` output (Docker Hub)
- [ ] `docker compose up` output
- [ ] `docker ps` showing both containers running
- [ ] Browser showing the Task Board at port 5000
- [ ] Docker Hub showing the pushed image
- [ ] Adding a task, bringing down containers, bringing back up (persistence proof)

### Part II
- [ ] Jenkins dashboard
- [ ] Jenkins pipeline configuration screen
- [ ] GitHub webhook settings
- [ ] GitHub push triggering the Jenkins build automatically
- [ ] All pipeline stages passing (green)
- [ ] `docker ps` showing jenkins containers on ports 5001/3307
- [ ] Browser showing Task Board at port 5001

---

## 🔗 GOOGLE FORM SUBMISSION

Submit your URLs here:
https://forms.gle/ubA9DRzQSudr2qhY6

URLs to include:
- **Part I:** `http://<EC2-PUBLIC-IP>:5000`
- **Part II (GitHub repo):** `https://github.com/YOUR_USERNAME/hassan-taskboard`
- Add `qasimalik@gmail.com` as a collaborator to your GitHub repo

---

## ⚠️ IMPORTANT REMINDERS

1. **Part I must be UP** when you submit — leave `docker compose up -d` running
2. **Part II must be DOWN initially** — Jenkins will bring it up when triggered
3. Add the instructor as GitHub collaborator so they can push to trigger the pipeline
4. Make sure EC2 Security Group allows ports: **5000, 5001, 8080**

TEST 1
