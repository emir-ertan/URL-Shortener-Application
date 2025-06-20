# URL Shortener Application

This document describes the architecture of a simple URL shortener application to be developed using Python, Flask, and SQLite.

## 1. Project Directory Structure

```
url-shortener/
├── app.py
├── database.py
├── templates/
│   └── index.html
└── static/
    └── css/
        └── bootstrap.min.css (or CDN usage)
    └── js/
        └── bootstrap.bundle.min.js (or CDN usage)
```

- `app.py`: The main Flask application file. Route definitions, request handling logic, and database interactions will be located here.
- `database.py`: Module to manage database connections, table creation, and data insertion/querying operations.
- `templates/`: Directory containing HTML template files.
    - `index.html`: The main page template that will display the URL shortening form and results.
- `static/`: Directory containing static files like CSS and JavaScript.
    - `css/`: CSS files. Bootstrap CSS can be placed here or a CDN can be used.
    - `js/`: JavaScript files. Bootstrap JS can be placed here or a CDN can be used.

## 2. Database Schema (SQLite)

The application will use an SQLite database file named `urls.db` to store URL data. There will be a single table named `urls` in the database.

**Table: `urls`**

| Column Name    | Data Type          | Constraints                 | Description                               |
|--------------|--------------------|------------------------------|----------------------------------------|
| `id`         | INTEGER            | PRIMARY KEY AUTOINCREMENT    | Unique record identifier               |
| `original_url` | TEXT               | NOT NULL                     | The original URL to be shortened       |
| `short_code` | TEXT               | UNIQUE NOT NULL              | The generated unique short code        |

## 3. Flask Application Structure

The application will include the following basic routes:

- **`/` (GET):** Displays the home page. A form for the user to enter a URL and an optional list of previously shortened URLs will be located here.
- **`/shorten` (POST):** Handles POST requests from the form on the home page.
    - Retrieves the original URL entered by the user.
    - Generates a unique short code for this URL.
    - Saves the original URL and short code to the database.
    - Displays the generated short URL to the user (usually by redirecting back to the home page or showing results).
- **`/<short_code>` (GET):** Handles requests for shortened URLs.
    - Retrieves the `<short_code>` value from the URL.
    - Searches the database for the original URL corresponding to this short code.
    - If the original URL is found, redirects the user to this URL.
    - If the short code is not found in the database, it can display an error page.
- **`/delete/<short_code>` (POST):** Handles POST requests to delete a shortened URL.
    - Retrieves the `<short_code>` value from the URL.
    - Deletes the corresponding entry from the database.
    - Redirects the user back to the home page.

## 4. Libraries to be Used

- **Flask:** Micro web framework to be used for developing the web application.
- **sqlite3:** Module included in Python's standard library that allows interaction with SQLite databases.
- **secrets:** Can be used to generate secure random short codes (or other modules like uuid, random can be considered).
- **Bootstrap:** CSS framework to be used for frontend design. Can be used via CDN or downloaded to the project's `static` directory.

This architecture forms the basic structure of the application. Coding will be done according to this structure in the following steps.

## 5. Installation and Setup

Here are the steps to get the URL Shortener Application up and running:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd url-shortener
   ```
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   python app.py
   ```