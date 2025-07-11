from flask import Flask, render_template, request, redirect, url_for
import sources

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        part_number = request.form.get("part_number", "").strip()
        selected_sources = request.form.getlist("sources")

        urls = []
        if part_number and selected_sources:
            for name in selected_sources:
                url_template = sources.SOURCES.get(name)
                if url_template:
                    url = url_template.format(part_number)
                    urls.append(url)
            return render_template("results.html", urls=urls)

    return render_template("index.html", sources=sources.SOURCES.keys())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
