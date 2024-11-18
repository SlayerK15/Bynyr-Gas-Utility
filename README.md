# Gas Utility Customer Service Portal

A Django-based web application for managing customer service requests for a gas utility company. The application allows customers to submit service requests online, track their status, and enables customer service representatives to manage and respond to these requests efficiently.

## Features

- User Authentication (Customer & Staff)
- Service Request Management
- Request Status Tracking
- File Attachments
- Customer Dashboard
- Staff Portal
- Notification System
- Request Timeline View
- Responsive Design

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SlayerK15/Bynyr-Gas-Utility.git
cd Bynyr-Gas-Utility
```

2. Create a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create environment variables file (.env) in the project root:
```bash
SECRET_KEY=your_secret_key_here
DEBUG=True
```

5. Apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Create required directories:
```bash
mkdir media
mkdir static
```

8. Collect static files:
```bash
python manage.py collectstatic
```

## Running the Development Server

1. Ensure your virtual environment is activated
2. Start the development server:
```bash
python manage.py runserver
```
3. Access the application at `http://127.0.0.1:8000`

## Project Structure

```
gas_utility/
├── accounts/            # User account management
├── requests/            # Service request handling
├── staff/              # Staff portal functionality
├── tracking/           # Request tracking and notifications
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, images)
├── media/              # User-uploaded files
└── gas_utility/        # Project settings and configuration
```

## Usage

### For Customers:
1. Register a new account
2. Log in to your dashboard
3. Create new service requests
4. Track request status
5. View request history
6. Receive notifications

### For Staff:
1. Log in with staff credentials
2. Access the staff dashboard
3. Manage service requests
4. Update request status
5. Assign requests to CSRs
6. Add internal notes

## API Endpoints

The application provides RESTful APIs for:
- User management
- Service request operations
- Status updates
- Notifications

Detailed API documentation is available at `/api/docs/` when running the server.

## Development

To contribute to this project:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## Testing

Run the test suite:
```bash
python manage.py test
```

## Security Considerations

- The default `SECRET_KEY` should be changed in production
- Debug mode should be disabled in production
- Implement proper SSL/TLS in production
- Regular security updates should be applied
- Proper access controls are implemented but should be reviewed

## Deployment

For production deployment:

1. Update `settings.py`:
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS`
   - Configure production database
   - Set up proper email backend

2. Set up proper web server (e.g., Nginx/Apache)
3. Configure WSGI server (e.g., Gunicorn)
4. Set up SSL/TLS
5. Configure static/media file serving
6. Set up proper database backup

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please submit issues through the GitHub issue tracker or contact the development team.
