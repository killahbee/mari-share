import os
from application import app

app.debug = app.config["DEBUG"]
app.run(host='0.0.0.0', port=8080)