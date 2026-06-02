from flask import Flask, render_template, request

app = Flask(__name__)

history = []


def check_url(url):

    score = 0
    checks = []

    # HTTPS Check
    if url.startswith("https://"):
        checks.append("✔ HTTPS Secure")
    else:
        score += 10
        checks.append("❌ No HTTPS")

    # Suspicious Symbols
    suspicious_symbols = ["@", "_"]

    found_symbol = False

    for symbol in suspicious_symbols:
        if symbol in url:
            score += 20
            found_symbol = True

    if found_symbol:
        checks.append("❌ Suspicious symbols found")
    else:
        checks.append("✔ No suspicious symbols")

    # URL Length
    if len(url) > 75:
        score += 15
        checks.append("❌ URL too long")
    else:
        checks.append("✔ URL length normal")

    # Suspicious Keywords
    suspicious_words = [
        "login",
        "verify",
        "bank",
        "update",
        "secure",
        "signin"
    ]

    keyword_found = False

    for word in suspicious_words:
        if word in url.lower():
            score += 20
            keyword_found = True

    if keyword_found:
        checks.append("❌ Suspicious keywords found")
    else:
        checks.append("✔ No suspicious keywords")

    # Too many numbers
    digit_count = sum(c.isdigit() for c in url)

    if digit_count > 6:
        score += 15
        checks.append("❌ Too many numbers")
    else:
        checks.append("✔ URL format looks normal")

    # Final Result
    if score >= 60:
        result = "Phishing Website ❌"
        color = "red"
        tip = "Do not enter passwords or personal information."

    elif score >= 30:
        result = "Suspicious Website ⚠️"
        color = "orange"
        tip = "Be careful before logging in."

    else:
        result = "Safe Website ✅"
        color = "lightgreen"
        tip = "Website looks safe."

    history.append({
        "url": url,
        "result": result
    })

    return result, score, checks, tip, color


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    score = 0
    checks = []
    tip = ""
    color = ""

    if request.method == "POST":

        url = request.form["url"]

        result, score, checks, tip, color = check_url(url)

    return render_template(
        "index.html",
        result=result,
        score=score,
        checks=checks,
        tip=tip,
        color=color,
        history=history
    )


if __name__ == "__main__":
    app.run(debug=True)