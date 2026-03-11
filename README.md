# MLSecOps CI/CD Pipeline

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Security](https://img.shields.io/badge/security-ModelScan%20%7C%20Gitleaks-blue)
![Cloud](https://img.shields.io/badge/deployment-AWS%20ECR%20%7C%20EC2-orange)

<img width="2760" height="1504" alt="ML" src="https://github.com/user-attachments/assets/a5786629-d670-4eb2-bb90-1ab77ab6daf3" />

## 🚀 Overview
As machine learning becomes the core of modern applications, securing the ML lifecycle is critical. This project demonstrates a fully automated, event-driven **DevSecOps pipeline** designed to secure AI models before they reach a production cloud environment. 

Moving beyond traditional post-deployment compliance auditing, this architecture engineers compliance directly into the build phase. It enforces strict "Shift-Left" security principles to automatically detect hardcoded secrets, analyze ML models for embedded malware, package the application, and securely deploy it to AWS via least-privilege IAM roles.

This architecture serves as the foundational deployment engine for highly secure, enterprise-grade AI cybersecurity SaaS platforms.

## 🛠️ Technology Stack
* **Continuous Integration / Automation:** GitHub Actions
* **Application Security (AppSec):** Gitleaks (Secret Scanning)
* **Machine Learning Security (MLSec):** Protect AI ModelScan (Vulnerability & Malware Scanning)
* **Containerization:** Docker
* **Cloud Infrastructure (AWS):**
  * **Amazon ECR:** Private, secure container registry for artifact storage.
  * **Amazon EC2:** Compute instance provisioned with strict, read-only IAM instance profiles for live execution.
  * **AWS IAM:** Temporary credential management and zero-standing-privilege access control.

## ⚙️ Pipeline Architecture & Workflow
1. **Code Commit:** A developer pushes ML models (`.pkl`, `.joblib`, `.onnx`) and inference code to the repository.
2. **Automated Security Gates:** GitHub Actions automatically intercepts the build:
   * **Credential Verification:** Runs `Gitleaks` to ensure no AWS access keys or passwords exist in the source code.
   * **Model Integrity Analysis:** Runs `ModelScan` to verify the AI models do not contain malicious code, unsafe opcodes, or deserialization vulnerabilities.
3. **Secure Containerization:** Upon passing all security checks, the pipeline builds a standardized Docker image.
4. **Cloud Deployment:** The pipeline authenticates with AWS using secure GitHub Secrets and pushes the container to a private Amazon ECR repository.
5. **Production Execution:** The container is pulled and executed on an Amazon EC2 server via secure, identity-based access.

## 🧪 Security Validation: The "Poison Pickle" RCE Test
To validate the "Fail-Closed" design of this pipeline, a simulated cyberattack was conducted using a "Poisoned Pickle" injection vector.



* **The Attack:** A Python script generated a malicious `.pkl` file containing an unsafe `__reduce__` method designed to execute an arbitrary Remote Code Execution (RCE) command (`os.system`).
* **The Defense:** The automated `ModelScan` gateway successfully introspected the binary, identified the `CRITICAL` vulnerability (Unsafe operator 'system' from module 'posix'), and immediately triggered Exit Code 1.
* **The Result:** The pipeline successfully blocked the infected model, proving that compromised assets cannot bypass the CI/CD gateway to reach the cloud environment.
