# 🔗 URL Shortener

A **simple, fast, and scalable URL Shortener** built using **Python (Flask)**.  
This application allows users to convert long URLs into short, shareable links and redirects them efficiently.

---

## 🚀 Features

✨ Shorten long URLs into compact links  
🔁 Instant redirection to original URLs  
📊 Database-backed storage for persistence  
🎨 Clean UI using HTML & CSS  
⚡ Lightweight & fast Flask backend  

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|-----------|
| 🧠 Backend | Python, Flask |
| 🗄️ Database | SQLite |
| 🎨 Frontend | HTML, CSS |
| 🔧 Utilities | Custom URL generator |

---

## 📂 Project Structure

url_shortner/
│
├── app.py # Main Flask application
├── models.py # Database models
├── utils.py # Utility functions (short URL generator)
├── requirements.txt # Project dependencies
│
├── templates/ # HTML templates
├── static/ # CSS & static assets
├── instance/ # Database instance
└── README.md # Project documentation

yaml
Copy code

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/aryan-26-prog/url_shortner.git
cd url_shortner
2️⃣ Create Virtual Environment (Recommended)
bash
Copy code
python -m venv venv
source venv/bin/activate     # On Linux/Mac
venv\Scripts\activate        # On Windows
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run the Application
bash
Copy code
python app.py
🔗 Open browser and visit:
👉 http://127.0.0.1:5000

🧪 How It Works
User enters a long URL

App generates a unique short code

Short URL is stored in database

Visiting the short URL redirects to original link

🌟 Future Enhancements
🚀 User authentication
📈 Click analytics & tracking
⏰ URL expiration feature
🌍 Custom aliases for URLs
☁️ Cloud deployment (Render / Railway)

🤝 Contributing
Contributions are welcome!
Feel free to fork, raise issues, or submit pull requests.

📄 License
This project is licensed under the MIT License.

👨‍💻 Author
Aryan Naik
💼 Computer Science & Engineering Undergraduate
🔗 GitHub: aryan-26-prog

⭐ If you like this project, don't forget to star the repository!
