# MLSecOps CI/CD Pipeline

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Security](https://img.shields.io/badge/security-ModelScan%20%7C%20Gitleaks-blue)
![Cloud](https://img.shields.io/badge/deployment-AWS%20ECR%20%7C%20EC2-orange)

<img width="2760" height="1504" alt="ML" src="https://github.com/user-attachments/assets/a5786629-d670-4eb2-bb90-1ab77ab6daf3" />

## 🚀 Overview
As machine learning becomes the core of modern applications, securing the ML lifecycle is critical. This project demonstrates a fully automated, event-driven **DevSecOps pipeline** designed to secure AI models before they reach a production cloud environment. 

Moving beyond traditional post-deployment compliance auditing, this architecture engineers compliance directly into the build phase. It enforces strict "Shift-Left" security principles using a 3-stage automated gateway to detect hardcoded secrets, analyze Python application code for vulnerabilities, and scan ML models for embedded malware prior to containerization and AWS deployment.

## 🛠️ Technology Stack
* **Continuous Integration / Automation:** GitHub Actions
* **Application Security (AppSec):**
  * **Gitleaks:** Secret & Credential Scanning
  * **Bandit:** Static Application Security Testing (SAST) for Python
* **Machine Learning Security (MLSec):** * **Protect AI ModelScan:** ML Vulnerability & Malware Scanning
* **Containerization:** Docker
* **Cloud Infrastructure (AWS):** Amazon ECR, Amazon EC2, AWS IAM (Zero-standing privileges)

## ⚙️ Pipeline Architecture & Workflow
1. **Code Commit:** A developer pushes ML models or Python training scripts (`train.py`) to the repository.
2. **Automated Security Gates (The 3-Stage Filter):** GitHub Actions automatically intercepts the build:
   * **Stage 1 - Credential Verification:** `Gitleaks` sweeps the repository to ensure no AWS access keys or passwords exist in the source code.
   * **Stage 2 - SAST:** `Bandit` analyzes the raw Python code for logic flaws, weak cryptography, and unsafe module imports.
   * **Stage 3 - Model Integrity:** `ModelScan` introspects the compiled AI models (`.pkl`, `.joblib`, etc.) to verify they do not contain malicious code or deserialization vulnerabilities.
3. **Secure Containerization:** Upon passing all security checks, the pipeline builds a standardized Docker image.
4. **Cloud Deployment:** The pipeline authenticates with AWS via dynamically referenced GitHub Secrets and pushes the container to a private Amazon ECR vault.

## 🧪 Threat Simulation & Exception Handling
To ensure the pipeline operates with a strict "Fail-Closed" design, rigorous security testing was conducted during development:

* **Simulated RCE Attack (Mitigated):** A "Poisoned Pickle" injection vector was introduced to the pipeline. The `ModelScan` gateway successfully introspected the binary, identified the `CRITICAL` vulnerability (Unsafe operator `system` from module `posix`), and immediately triggered Exit Code 1, successfully blocking the deployment. The malicious script has since been removed from the production branch.
* **Security Triage & Exception Handling:** During SAST scanning, Bandit flagged the use of the `pickle` module (`B403`). Because the generation of the model is intentional and protected by downstream MLSec scanning, an explicit inline security exception (`# nosec B403`) was engineered into the code. This demonstrates mature alert triage and false-positive management.

* **The Attack:** A Python script generated a malicious `.pkl` file containing an unsafe `__reduce__` method designed to execute an arbitrary Remote Code Execution (RCE) command (`os.system`).
* **The Defense:** The automated `ModelScan` gateway successfully introspected the binary, identified the `CRITICAL` vulnerability (Unsafe operator 'system' from module 'posix'), and immediately triggered Exit Code 1.
* **The Result:** The pipeline successfully blocked the infected model, proving that compromised assets cannot bypass the CI/CD gateway to reach the cloud environment.

## 🚧 Current Limitations & Future Scope
While this architecture provides a robust baseline for MLSecOps, it has architectural boundaries that would need to be addressed for hyperscale enterprise use:

* **Compute Constraints (Runner Limits):** GitHub-hosted runners have memory and storage limits (typically 7GB RAM / 14GB SSD). Compiling Docker containers for massive Large Language Models (LLMs) weighing tens of gigabytes would cause out-of-memory (OOM) failures. *Future Fix: Implement self-hosted AWS runners with larger EC2 instance types.*
* **Static vs. Runtime Security:** This pipeline excels at Static Application Security Testing (SAST) and static model analysis. However, it does not currently test for runtime vulnerabilities, such as Prompt Injection, Data Poisoning, or adversarial evasion attacks against the live API.
* **Alert Fatigue & False Positives:** Tools like Bandit and Gitleaks rely on pattern matching, which can generate false positives (as mitigated in this project via inline exceptions). In a large organization, this requires a dedicated triage team to prevent deployment bottlenecks.
* **Deployment Orchestration:** The current CD pipeline pushes to a single Amazon EC2 instance. It lacks High Availability (HA), automated rollbacks, and auto-scaling. *Future Fix: Migrate the deployment target from standalone EC2 to Amazon EKS (Kubernetes) or AWS ECS.*
