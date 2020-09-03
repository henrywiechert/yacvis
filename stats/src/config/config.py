import os

## App settings
name = "Covid19"
host = "0.0.0.0"
port = int(os.environ.get("PORT", 8050))
debug = True

fontawesome = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'

## File system
root = os.path.dirname(os.path.dirname(__file__)) + "/"
