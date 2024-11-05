# BlogProject

## Overview

`BlogProject` is a Django web application designed for managing blogs. The project includes features for user authentication, blog posts, comments, suggestions, and reports. It leverages Django 5.0.7 and includes various customizations such as a custom user model and media file handling.

## Features

- User authentication and custom user model.
- Blog post management.
- Commenting on posts.
- Suggestions and report handling.
- Media file management (e.g., file uploads).

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Django 5.0.7
- A virtual environment (recommended)

### Installation

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd BlogProject
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the environment variables:**

    Create a `.env` file in the root directory with the following content:

    ```env
    SECRET_KEY=your_secret_key
    EMAIL_HOST_USER=your_email@example.com
    EMAIL_HOST_PASSWORD=your_email_password
    ```

5. **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (optional but recommended for accessing the admin portal):**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    Access the application at `http://127.0.0.1:8000/`.

## Configuration

### Settings

- **`SECRET_KEY`**: Used for cryptographic operations. Keep it secret.
- **`DEBUG`**: Set to `True` for development. Set to `False` for production.
- **`ALLOWED_HOSTS`**: List of allowed hosts for the application.
- **`MEDIA_URL`**: URL for media files.
- **`MEDIA_ROOT`**: Directory for storing uploaded media files.
- **`EMAIL_BACKEND`**: Email backend configuration for sending emails.

### Custom User Model

The project uses a custom user model `BlogApp.User`. Ensure that any references to the user model in your code align with this custom model.

### Static Files

- **`STATIC_URL`**: URL for serving static files.
- **`STATICFILES_DIRS`**: List of directories where Django will look for static files.

## URLs

- **`/login/`**: Login page.
- **`/admin/`**: Admin portal.
- **`/role/user/`**: Redirects to user role page.
- **`/role/admin/`**: Redirects to admin role page.
- **`/role/moderator/`**: Redirects to moderator role page.

## Troubleshooting

- **NoReverseMatch**: Ensure that URL names used in `{% url %}` template tags match those defined in `urls.py`.
- **Static files not updating**: Clear the browser cache and check if the static files are correctly served.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Django 5.0.7 for providing the framework and tools for this project.
- All contributors and libraries used in the development of this project.

For more details, refer to the [Django Documentation](https://docs.djangoproject.com/en/5.0/).

