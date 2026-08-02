from flask import Flask, render_template, request

from backend.api import search_colleges

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html")


@app.route("/roi")
def roi():
    return render_template("about_roi.html")


@app.route("/results")
def results():

    state = request.args.get("state")
    school_type = request.args.get("school_type")
    major = request.args.get("major")
    degree_level = request.args.get("degree_level")
    min_earnings = request.args.get("min_earnings", type=int)
    max_debt = request.args.get("max_debt", type=int)
    max_tuition = request.args.get("max_tuition", type=int)

    colleges = search_colleges(
        state=state,
        school_type=school_type,
        major=major,
        degree_level=degree_level,
        min_earnings=min_earnings,
        max_debt=max_debt,
        max_tuition=max_tuition,
    )

    tuition_values = [
        college["tuition"]
        for college in colleges
        if college["tuition"] is not None
    ]

    earnings_values = [
        college["earnings"]
        for college in colleges
        if college["earnings"] is not None
    ]

    debt_values = [
        college["debt"]
        for college in colleges
        if college["debt"] is not None
    ]

    average_tuition = (
        round(sum(tuition_values) / len(tuition_values))
        if tuition_values else 0
    )

    average_earnings = (
        round(sum(earnings_values) / len(earnings_values))
        if earnings_values else 0
    )

    average_debt = (
        round(sum(debt_values) / len(debt_values))
        if debt_values else 0
    )

    return render_template(
        "results.html",
        colleges=colleges,
        average_tuition=average_tuition,
        average_earnings=average_earnings,
        average_debt=average_debt,
    )


if __name__ == "__main__":
    app.run(debug=True)
