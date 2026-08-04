from flask import Flask, render_template, request


from backend.analysis import add_roi_data
from backend.api import get_colleges_by_ids, search_colleges

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
    colleges = add_roi_data(colleges) 

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
@app.route("/roi-analysis")
def roi_analysis():
    selected_ids = request.args.getlist("school_ids")

    # Remove duplicates while preserving selection order.
    selected_ids = list(dict.fromkeys(selected_ids))

    if not selected_ids:
        return render_template(
            "roi_analysis.html",
            colleges=[],
            chart_data={},
            error_message="Select at least one school from the results page.",
        )

    # Prevent an extremely large comparison/chart request.
    selected_ids = selected_ids[:10]

    colleges = get_colleges_by_ids(selected_ids)
    colleges = add_roi_data(colleges)

    valid_roi_colleges = [
        college
        for college in colleges
        if college["roi_score"] is not None
    ]

    chart_data = {
        "labels": [
            college["name"]
            for college in valid_roi_colleges
        ],
        "tuition": [
            college["tuition"] or 0
            for college in valid_roi_colleges
        ],
        "earnings": [
            college["earnings"] or 0
            for college in valid_roi_colleges
        ],
        "debt": [
            college["debt"] or 0
            for college in valid_roi_colleges
        ],
        "roi_scores": [
            college["roi_score"]
            for college in valid_roi_colleges
        ],
    }

    return render_template(
        "roi_analysis.html",
        colleges=colleges,
        chart_data=chart_data,
        error_message=None,
    )

if __name__ == "__main__":
    app.run(debug=True)
