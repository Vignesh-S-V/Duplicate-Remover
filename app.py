import os
from flask import Flask, render_template, request, send_file, redirect
from config import UPLOAD_FOLDER
from utils.file_handler import allowed_file, read_file, save_file
from services.cleaner import DataCleaner
import uuid

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        example_file = request.files.get("example_file")
        raw_file = request.files.get("raw_file")

        if not example_file or not raw_file:
            return "Both files are required"

        if not (allowed_file(example_file.filename) and allowed_file(raw_file.filename)):
            return "Invalid file type"

        example_path = os.path.join(
            UPLOAD_FOLDER, f"example_{uuid.uuid4()}_{example_file.filename}"
        )
        raw_path = os.path.join(
            UPLOAD_FOLDER, f"raw_{uuid.uuid4()}_{raw_file.filename}"
        )

        example_file.save(example_path)
        raw_file.save(raw_path)

        # Read files
        example_df = read_file(example_path)
        raw_df = read_file(raw_path)

        # Clean
        cleaned_df = DataCleaner.align_to_template(example_df, raw_df)

        output_filename = f"cleaned_{uuid.uuid4()}.xlsx"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)

        save_file(cleaned_df, output_path)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)