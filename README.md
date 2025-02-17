# **Gaming News Aggregator**

## **Description**

The **Gaming News Aggregator** is a web application that scrapes gaming news(currently, it only retrieves news related to the PC platform.) from multiple websites every 12 minutes, stores the data in a PostgreSQL database, and displays it in a clean, user-friendly interface. It uses a **Flask** backend with **Gunicorn** for deployment, a **Next.js** frontend, and a **PostgreSQL** database hosted on **Supabase**. The project is containerized using **Docker** to simplify deployment.

## **Tech Stack**

- **Backend**: Flask, Gunicorn, Marshmallow, SQLAlchemy
- **Frontend**: Next.js, Tailwind CSS
- **Database**: PostgreSQL (hosted on Supabase)
- **Web Scraping**: BeautifulSoup, aiohttp
- **Deployment**: Docker, Render (Flask), Vercel (Next.js)

## **Features**

- Scrapes gaming news from multiple sources every 12 minutes.
- Stores scraped articles in a PostgreSQL database.
- RESTful API to fetch the latest gaming news.
- User-friendly interface built with Next.js and Tailwind CSS.
- Features planned for future: user authentication, search, notifications, and an analytics dashboard.

### Planned Features:

- **User Authentication**: Allow users to create accounts and save their favorite news articles.
- **Multi-Platform Support**: Support additional platforms including PC, PlayStation, Xbox, and Switch.
- **Search Functionality**: Enable users to search for specific news articles.
- **Notifications**: Send email or push notifications for breaking news.
- **Game Data from IGDB API**: Expanded game details such as trailers, reviews, and more user-specific game recommendations.

## **Setup & Installation**

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Set up environment variables**:
   Create a `.env` file in the root directory and add the following:

   - **Backend**:
     - `DATABASE_URL`: Connection string for PostgreSQL.
     - `FLASK_ENV`: Set to `production` when deploying.
   - **Frontend**:
     - `API_URL`: URL for your backend API (e.g., `https://your-backend-url`).

3. **Running with Docker**:

   - Ensure Docker and Docker Compose are installed on your machine.
   - Build and run the containers:
     ```bash
     docker-compose up --build
     ```

4. **Accessing the application**:
   - Frontend will be available on `http://localhost:3000`.
   - Backend will be available on `http://localhost:5000`.

## **API Endpoints**

1. **Initialize the database**:
   POST request to `/api/initialize` to set up the database with the required models.
2. **Start scraping manually**:
   POST request to `/api/scrape` to initiate the scraping process.

3. **Fetch all gaming news**:
   ```bash
   GET http://localhost:5000/news
   ```

## **Deployment**

### **Flask Backend**

To deploy the Flask backend using Docker:

1. **Build and run the backend**:

   ```bash
   docker build -t backend .
   docker run -p 5000:5000 backend
   ```

2. **Using Gunicorn**:
   The app is configured to run with Gunicorn for better performance in production:
   ```bash
   gunicorn --bind 0.0.0.0:5000 run:app
   ```

### **Next.js Frontend**

To deploy the Next.js frontend using Docker:

1. **Build and run the frontend**:

   ```bash
   docker build -t frontend .
   docker run -p 3000:3000 frontend
   ```

2. **Vercel Deployment**:
   Vercel automatically builds and deploys the frontend for you if you connect your GitHub repository to Vercel.

## **Contributing**

This project is open-source! Feel free to fork it, create pull requests, and help improve it. Contributions, bug fixes, and feature requests are always welcome.

## License

[MIT License](LICENSE)