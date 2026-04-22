import uvicorn

from .bootstrap import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run('notification_email_service.main:app', host='0.0.0.0', port=9090, reload=False)