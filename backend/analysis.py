def calculate_roi(college, years_of_tuition=4, earnings_years=10):
    """
    Calculate an estimated education ROI.

    Estimated investment:
        four years of tuition + median student debt

    Estimated return:
        ten years of median annual earnings

    ROI:
        ((return - investment) / investment) * 100

    This is a comparison estimate, not a prediction of an individual
    student's financial outcome.
    """
    tuition = college.get("tuition")
    earnings = college.get("earnings")
    debt = college.get("debt")

    if tuition is None or earnings is None:
        return None

    # Treat missing debt as zero so a college can still receive an estimate.
    debt = debt or 0

    estimated_tuition_cost = tuition * years_of_tuition
    estimated_total_cost = estimated_tuition_cost + debt
    estimated_earnings = earnings * earnings_years
    estimated_net_return = estimated_earnings - estimated_total_cost

    if estimated_total_cost <= 0:
        return None

    roi_percentage = (
        estimated_net_return / estimated_total_cost
    ) * 100

    return {
        "tuition_cost": round(estimated_tuition_cost),
        "total_cost": round(estimated_total_cost),
        "projected_earnings": round(estimated_earnings),
        "net_return": round(estimated_net_return),
        "roi_percentage": round(roi_percentage, 1),
    }


def add_roi_data(colleges):
    """
    Add ROI values to each college and assign ROI rankings.

    The original dictionaries are copied so the search results are not
    unexpectedly modified elsewhere.
    """
    analyzed_colleges = []

    for college in colleges:
        analyzed_college = college.copy()
        roi_data = calculate_roi(analyzed_college)

        analyzed_college["roi"] = roi_data
        analyzed_college["roi_score"] = (
            roi_data["roi_percentage"] if roi_data else None
        )

        analyzed_colleges.append(analyzed_college)

    ranked_colleges = sorted(
        analyzed_colleges,
        key=lambda college: (
            college["roi_score"] is not None,
            college["roi_score"] or 0,
        ),
        reverse=True,
    )

    current_rank = 1

    for college in ranked_colleges:
        if college["roi_score"] is not None:
            college["roi_rank"] = current_rank
            current_rank += 1
        else:
            college["roi_rank"] = None

    return ranked_colleges