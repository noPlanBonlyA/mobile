import uvicorn

from .bootstrap import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run('school_site.main:app', host='0.0.0.0', port=8080, reload=False)