# 🦙 Mini-Llama CTF

### &#x20;LLM Security Challenges

Mini-Llama CTF is a hands-on, CTF-style project designed to explore vulnerabilities in Large Language Model (LLM) applications. It contains three challenges across Easy, Medium, and Hard difficulty levels, inspired by security risks covered in the OWASP Top 10 for LLM Applications.

<p align="center">

</p>

---

## 📌 Project Details

- **Project Name:** Mini-Llama CTF
- **Category:** AI Security / LLM Application Security
- **Interface:** Streamlit Web Application
- **Programming Language:** Python
- **LLM Runtime:** Ollama
- **Recommended Model:** `llama3.1:8b`
- **Database:** SQL
- **Data Processing:** Pandas

## 🎯 Challenges

| Difficulty | Vulnerability         |
| ---------- | --------------------- |
| 🟢 Easy    | System Prompt Leakage |
| 🟡 Medium  | AI Misinformation     |
| 🔴 Hard    | Excessive Agency      |

### 1. Easy — System Prompt Leakage

Explore whether carefully crafted user inputs can cause the LLM to reveal hidden system instructions.

**Learning objective:** Understand why system prompts should not be treated as secure storage for secrets or sensitive information.

### 2. Medium — AI Misinformation

Explore how an LLM can generate false or misleading information and why model responses should be evaluated rather than blindly trusted.

**Learning objective:** Understand the risks of unreliable AI-generated information and the importance of verification.

### 3. Hard — Excessive Agency

Explore a fictional scenario in which the LLM is prompted to use an imaginary tool or perform an unauthorized action.

**Important:** This challenge uses a fictional tool scenario for educational purposes. No actual external tool is connected, and no real-world action is executed.

**Learning objective:** Understand why AI applications need appropriate permissions, restricted capabilities, and safeguards around consequential actions.

These challenges are educational demonstrations inspired by OWASP LLM application security risks. The challenge IDs above are project-defined labels, not official OWASP identifiers.

---

## 🛠️ Technology Stack

| Technology   | Purpose                               |
| ------------ | ------------------------------------- |
| Python       | Application and challenge logic       |
| Streamlit    | Interactive web interface             |
| Ollama       | Local LLM execution                   |
| Llama 3.1 8B | Model used for challenge interactions |
| Pandas       | Data processing                       |
| SQL          | Storing submitted prompts             |

## ✨ Key Features

- Three LLM security challenges with increasing difficulty.
- Local AI inference through Ollama.
- Interactive Streamlit interface.
- SQL database for storing user-submitted prompts.
- Challenge-specific results and vulnerability demonstrations.
- Practical exploration of LLM security risks.

---

## 🚀 Installation and Setup

### Prerequisites

- Python installed
- Git installed
- Ollama installed
- Sufficient system resources to run the selected LLM locally

### Step 1: Download the LLM

Install and start Ollama from [ollama.com](https://ollama.com/).

Pull the recommended model:

```bash
ollama pull llama3.1:8b
```

**Recommended model:** `llama3.1:8b`

Using this model is recommended for the intended project experience. Actual response quality and speed depend on your hardware, model configuration, and challenge prompts.

### Step 2: Clone the Repository

```
git clone https://github.com/OmDorugade/AI-Security-Engineer-Projects.git
cd AI-Security-Engineer-Projects
```

Replace `<your-username>` with your GitHub username.

### Step 3: Create a Virtual Environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux:**

```
python3 -m venv .venv
source .venv/bin/activate
```

### Step 4: Install Dependencies

```
pip install -r requirements.txt
```

### Step 5: Run the Model

```
ollama run llama3.1:8b
```


### Step 6: Run the Application

Make sure Ollama is running and the model is available, then start the Streamlit application:

```
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```
http://localhost:8501
```

---

## 🗄️ Database

The project uses SQL to store submitted prompts for later review.

The database supports prompt storage associated with the challenge workflow. The exact schema and stored fields depend on the implementation.

Do not submit real passwords, API keys, confidential information, or other sensitive data.

## 📚 Learning Objectives

By completing this project, learners can:

- Explore common vulnerabilities in LLM-powered applications.
- Understand system prompt leakage risks.
- Recognize misinformation in AI-generated responses.
- Learn why AI tool access requires security controls.
- Practice testing model behavior through interactive challenges.
- Understand how SQL can support application-level prompt logging.



## ⚠️ Disclaimer

This project is intended for educational purposes and authorized security research. The vulnerabilities are demonstrated in a controlled application. The Excessive Agency challenge uses a fictional tool scenario and does not execute real-world actions.

---

