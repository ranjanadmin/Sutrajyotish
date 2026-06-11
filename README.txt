
DEPLOYMENT STEPS
================

1. Copy:
templates/palmistry.html
to your:
templates/

2. Copy:
static/palmistry.js
to your:
static/js/

3. Add this route inside app.py ABOVE:
if __name__ == "__main__":

@app.route("/palmistry")
def palmistry():

    return render_template(
        "palmistry.html"
    )

4. Restart Flask

5. Open:
http://YOUR-IP:5000/palmistry
