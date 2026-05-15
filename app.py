from flask import Flask, render_template, request, redirect
import mysql.connector, os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ----------------------------
# File Upload Configuration
# ----------------------------
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXT = {"png", "jpg", "jpeg"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ----------------------------
# Database Connection
# ----------------------------
def get_cursor():
    """Creates a fresh MySQL connection each time."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",          # XAMPP default
        database="talentedo_db",
        port=3306
    )
    return db, db.cursor(buffered=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


# ----------------------------
# ROUTES
# ----------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/courses")
def courses():
    search = request.args.get("search", "")
    db, cursor = get_cursor()

    cursor.execute("SELECT id, course_name FROM courses")
    data = cursor.fetchall()

    # Filter search
    if search:
        data = [c for c in data if search.lower() in c[1].lower()]

    db.close()
    return render_template("courses.html", courses=data, search=search)


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/gallery", methods=["GET", "POST"])
def gallery():
    db, cursor = get_cursor()

    if request.method == "POST":
        if "image" not in request.files:
            return redirect("/gallery")

        file = request.files["image"]

        if file.filename == "":
            return redirect("/gallery")

        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)

            cursor.execute("INSERT INTO gallery (filename) VALUES (%s)", (filename,))
            db.commit()

        return redirect("/gallery")

    cursor.execute("SELECT filename FROM gallery")
    images = [i[0] for i in cursor.fetchall()]

    db.close()
    return render_template("gallery.html", images=images)


@app.route("/whychoose")
def whychoose():
    return render_template("whychoose.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    db, cursor = get_cursor()

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        course = request.form["course"]
        message = request.form["message"]

        cursor.execute(
            "INSERT INTO enquiries (name, phone, course, message) VALUES (%s, %s, %s, %s)",
            (name, phone, course, message)
        )
        db.commit()

        return redirect("/contact")

    db.close()
    return render_template("contact.html")


@app.route("/admin")
def admin():
    db, cursor = get_cursor()
    search = request.args.get("search", "")

    if search:
        cursor.execute("SELECT * FROM enquiries WHERE name LIKE %s", ("%" + search + "%",))
    else:
        cursor.execute("SELECT * FROM enquiries ORDER BY id DESC")

    data = cursor.fetchall()
    db.close()
    return render_template("admin.html", data=data, search=search)


@app.route("/delete/<int:id>")
def delete_entry(id):
    db, cursor = get_cursor()
    cursor.execute("DELETE FROM enquiries WHERE id=%s", (id,))
    db.commit()
    db.close()
    return redirect("/admin")


# ----------------------------
# Start Flask
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)