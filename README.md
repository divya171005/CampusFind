# CampusFind – Campus Lost & Found Portal

A web-based campus lost and found platform that helps students report missing belongings, post found items, and reconnect people with their lost possessions.

##  Live Demo

**Live Website:** https://campusfind-iylj.onrender.com

**GitHub Repository:** https://github.com/divya171005/CampusFind

##  About the Project

CampusFind is designed to make the process of finding lost belongings easier within a college campus. Students can report lost or found items, browse existing listings, search for specific belongings, and contact the person who posted a report.

The application provides a centralized platform that encourages students to help one another and makes lost-and-found management more accessible.

##  Features

- **Report Lost Items:** Publish details of missing belongings.
- **Report Found Items:** Share information about items found on campus.
- **Browse Listings:** View available lost and found reports.
- **Search Functionality:** Search using item names, descriptions, and locations.
- **Category Filters:** Filter reports by item category and type.
- **Contact Information:** Contact the person who posted a listing.
- **Mark as Resolved:** Update listings once an item has been returned.
- **Database Integration:** Store reports using MongoDB Atlas.

##  Tech Stack

| Technology | Purpose |
|---|---|
| HTML5 | Website structure |
| CSS3 | Styling and responsive design |
| JavaScript | Frontend interactions |
| Python | Backend programming |
| FastAPI | REST API development |
| MongoDB Atlas | Cloud database |
| Git & GitHub | Version control |
| Docker | Application containerization |
| GitHub Actions | CI/CD automation (planned) |

##  Project Structure

```text
CampusFind/
│
├── .gitignore
│
└── Campus-Lost-and-Found/
    ├── main.py
    ├── requirements.txt
    ├── Dockerfile
    ├── .dockerignore
    ├── .env.example
    ├── .gitignore
    ├── README.md
    │
    └── static/
        ├── index.html
        ├── style.css
        └── app.js
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/divya171005/CampusFind.git
```

### 2. Navigate to the application directory

```bash
cd CampusFind/Campus-Lost-and-Found
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file using `.env.example` as a template.

```env
MONGODB_URI=your_mongodb_connection_string
MONGODB_DATABASE=campus_lost_found
```

Never upload your `.env` file or database credentials to GitHub.

### 7. Run the application

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Check application and database status |
| GET | `/api/items` | Retrieve and filter listings |
| POST | `/api/items` | Create a new listing |
| PATCH | `/api/items/{item_id}/resolve` | Mark a listing as resolved |

Interactive API documentation is available at `/docs`.

##  Docker Setup

Build the Docker image:

```bash
docker build -t campusfind .
```

Run the container:

```bash
docker run --env-file .env -p 8000:8000 campusfind
```

Open http://localhost:8000.

##  DevOps Implementation

The project is being developed with a DevOps workflow involving:

- Git and GitHub for source code management.
- Docker for containerization.
- GitHub Actions for continuous integration and deployment.
- Cloud hosting for application deployment.
- MongoDB Atlas for cloud-based data persistence.

##  Future Enhancements

- Student authentication and authorization.
- Image uploads for lost and found items.
- Admin dashboard and report moderation.
- Email notifications for possible item matches.
- Improved security and access controls.

##  Author

**Divya**

B.Tech – Computer Science and Engineering (Data Science)

GitHub: https://github.com/divya171005

---

*CampusFind – Helping campus communities find what matters.*
