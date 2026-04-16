from flask import Flask, render_template, request

app = Flask(__name__)

def chatbot_response(user_input):
    user_input = user_input.lower()

    if "admission" in user_input:
        return "Admission requires FSC with minimum 60% marks and entry test clearance."

    elif "deadline" in user_input:
        return "Admission deadline is usually in August every year."

    elif "program" in user_input:
        return "We offer BS Computer Science, AI, and Software Engineering."

    elif "fee" in user_input:
        return "Fee depends on program, average is 50,000 - 80,000 per semester."

    else:
        return "Sorry, I don't understand. Please ask about admission, fee, or programs."


@app.route("/", methods=["GET", "POST"])
def index():
    response = ""

    if request.method == "POST":
        user_message = request.form["message"]
        response = chatbot_response(user_message)

    return render_template("index.html", response=response)


if __name__ == "__main__":
    app.run(debug=True)