```python
def calculate_roi(college, years_of_tuition=4, earnings_years=10):
    """
    Calculate an estimated return on investment (ROI) for a college.

    The estimate compares the expected cost of attending the college with
    projected earnings over a specified period.

    Calculation:
        investment = (annual tuition * years_of_tuition) + median student debt
        return = median annual earnings * earnings_years
        ROI = ((return - investment) / investment) * 100

    Args:
        college (dict): College data containing:
            - tuition: Annual tuition cost.
            - earnings: Median annual earnings.
            - debt: Median student debt. Missing debt is treated as zero.
        years_of_tuition (int, optional): Number of tuition-paying years.
            Defaults to 4.
        earnings_years (int, optional): Number of years used to project
            earnings. Defaults to 10.

    Returns:
        dict | None: ROI metrics containing tuition cost, total cost,
        projected earnings, net return, and ROI percentage. Returns None
        when tuition or earnings data is unavailable or when the estimated
        total cost is not positive.

    Note:
        This calculation is intended as a comparison estimate and should not
        be interpreted as a prediction of an individual student's financial
        outcome.
    """
    tuition = college.get("tuition")
    earnings = college.get("earnings")
    debt = college.get("debt")

    # Tuition and earnings are required to produce a meaningful estimate.
    if tuition is None or earnings is None:
        return None

    # Allow colleges with missing debt data to still receive an ROI estimate.
    debt = debt or 0

    estimated_tuition_cost = tuition * years_of_tuition
    estimated_total_cost = estimated_tuition_cost + debt
    estimated_earnings = earnings * earnings_years
    estimated_net_return = estimated_earnings - estimated_total_cost

    # Avoid division by zero or calculations based on invalid cost data.
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
    Calculate ROI metrics and assign ROI rankings to a collection of colleges.

    Each college dictionary is copied before ROI data is added, preventing
    the original search results from being modified. Colleges with valid ROI
    estimates are ranked from highest to lowest ROI. Colleges without enough
    data to calculate ROI are placed after ranked colleges and receive no rank.

    Args:
        colleges (iterable[dict]): College records to analyze.

    Returns:
        list[dict]: Copies of the college records enriched with:
            - roi: Detailed ROI metrics from ``calculate_roi``.
            - roi_score: ROI percentage used for sorting and ranking.
            - roi_rank: Position relative to colleges with valid ROI data.

    Ranking behavior:
        Rankings are sequential and based on descending ROI percentage.
        Colleges with unavailable ROI scores receive ``None`` for ``roi_rank``.

    Note:
        The input dictionaries are not modified.
    """
    analyzed_colleges = []

    for college in colleges:
        # Work with a copy so downstream analysis does not mutate source data.
        analyzed_college = college.copy()
        roi_data = calculate_roi(analyzed_college)

        analyzed_college["roi"] = roi_data
        analyzed_college["roi_score"] = (
            roi_data["roi_percentage"] if roi_data else None
        )

        analyzed_colleges.append(analyzed_college)

    # Rank colleges with valid ROI scores first, from highest to lowest.
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
```
