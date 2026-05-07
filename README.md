# Boom Blockers Games 🎮

Boom Blockers Games is a Flask-based gaming web application that combines a Python game engine with a web frontend.
The project contains:

* A Python game module
* A Flask web application
* Frontend integration
* Interactive gameplay mechanics

This README provides complete setup and running instructions for beginners.

---

# 📌 Project Overview

The project is divided into multiple parts:

```bash
boom-blockers-games/
│
├── client/             # Game logic and Python game files
│   └── game.py
│
├── frontend/           # Flask frontend application
│   └── app.py
│
├── website/            # Main VS Code working directory
│   └── app.py
│
├── static/             # CSS, JS, images
├── templates/          # HTML templates
├── requirements.txt    # Python dependencies
└── README.md
```

---

# 🚀 Features

* Flask-powered backend
* Interactive Python game
* Frontend web integration
* Beginner-friendly structure
* Easy local setup
* Lightweight architecture

---

# 🛠️ Technologies Used

* Python
* Flask
* HTML5
* CSS3
* JavaScript
* Jinja2 Templates

---

# 📦 Prerequisites

Before running the project, install:

* Python 3.10+
* pip
* Git
* VS Code (recommended)

---

# 🔽 Clone the Repository

```bash
git clone https://github.com/Partho-Kumar-Shaw/boom-blockers-games.git
```

Move into the project directory:

```bash
cd boom-blockers-games
```

---

# ⚙️ Create Virtual Environment (Recommended)

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 📥 Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

The project has multiple runnable modules.

---

# 🎮 Run the Game Module

Move into the client directory:

```bash
cd client
```

Run the game:

```bash
python game.py
```

---

# 🌐 Run the Frontend Flask App

Open a new terminal.

Move into frontend directory:

```bash
cd frontend
```

Run Flask app:

```bash
python app.py
```

---

# 💻 Running Inside VS Code

## Step 1

Open the project in VS Code.

---

## Step 2

Change terminal directory to:

```bash
website
```

Example:

```bash
cd website
```

---

## Step 3

Run Flask application:

```bash
python app.py
```

---

# 🌍 Access the Website

After running Flask app, open browser:

```bash
http://127.0.0.1:5000
```

or

```bash
http://localhost:5000
```

---

# 📂 Important Files

| File               | Purpose              |
| ------------------ | -------------------- |
| `game.py`          | Main game logic      |
| `app.py`           | Flask application    |
| `requirements.txt` | Project dependencies |
| `templates/`       | HTML pages           |
| `static/`          | CSS, JS, images      |

---

# 🐛 Common Errors & Fixes

---

## 1. ModuleNotFoundError

Install dependencies again:

```bash
pip install -r requirements.txt
```

---

## 2. Git Clone Error

If cloning fails with:

```bash
RPC failed; curl 56 Recv failure
```

Try:

```bash
git clone --depth 1 https://github.com/Partho-Kumar-Shaw/boom-blockers-games.git
```

---

## 3. Flask Not Found

Install Flask manually:

```bash
pip install flask
```

---

## 4. Port Already in Use

Change Flask port:

```python
app.run(port=5001)
```

---

# 🤝 Contributing

Contributions are welcome.

## Steps

1. Fork repository
2. Create branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push changes

```bash
git push origin feature-name
```

5. Open Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Partho Kumar Shaw

GitHub:
https://github.com/Partho-Kumar-Shaw

---

# ⭐ Support

If you like this project:

* Star the repository
* Fork it
* Share it with others

Happy Coding 🚀
