import re


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):

    if text is None:
        return ""

    text = str(text).strip()

    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"__", "", text)

    return text.strip()


# ============================================================
# EXTRACT RECOMMENDATIONS
# ============================================================

def extract_recommendations(response):

    recommendations = []

    if not response:
        return recommendations

    response = str(response).strip()

    # --------------------------------------------------------
    # Split recommendations using numbered items
    # --------------------------------------------------------

    blocks = re.split(
        r"\n\s*(?=\d+\.\s*)",
        response
    )

    for block in blocks:

        block = block.strip()

        if not block:
            continue

        # ====================================================
        # NAME
        # ====================================================

        name = ""

        name_match = re.search(
            r"(?:NAME|Name|Recommendation|Title)"
            r"\s*:\s*(.+?)(?=\n|$)",
            block,
            re.IGNORECASE
        )

        if name_match:

            name = name_match.group(1).strip()

        else:

            # Try numbered format
            numbered_match = re.search(
                r"^\d+\.\s*(.+?)(?=\n|$)",
                block
            )

            if numbered_match:

                name = numbered_match.group(1).strip()

        # ====================================================
        # SCORE
        # ====================================================

        score = 0

        # First try:
        # SCORE: 95
        # Score - 95
        score_match = re.search(
            r"(?:SCORE|Score|Suitability\s*Score|Rating)"
            r"\s*[:\-]?\s*(\d{1,3})",
            block,
            re.IGNORECASE
        )

        if score_match:

            try:

                score = int(
                    score_match.group(1)
                )

            except ValueError:

                score = 0

        else:

            # Try percentage format:
            # 95%
            percentage_match = re.search(
                r"\b(\d{1,3})\s*%",
                block
            )

            if percentage_match:

                try:

                    score = int(
                        percentage_match.group(1)
                    )

                except ValueError:

                    score = 0

            else:

                # Try format:
                # 95/100
                fraction_match = re.search(
                    r"\b(\d{1,3})\s*/\s*100\b",
                    block
                )

                if fraction_match:

                    try:

                        score = int(
                            fraction_match.group(1)
                        )

                    except ValueError:

                        score = 0

        # Keep score between 0 and 100

        score = max(
            0,
            min(score, 100)
        )

        # ====================================================
        # REASON
        # ====================================================

        reason = ""

        reason_match = re.search(
            r"(?:REASON|Reason|WHY|Why|Explanation)"
            r"\s*:\s*(.+?)(?="
            r"\n\s*(?:NAME|Name|Recommendation|Title|SCORE|Score|"
            r"Suitability\s*Score|Rating|REASON|Reason|WHY|Why|Explanation)"
            r"\s*:|\Z)",
            block,
            re.IGNORECASE | re.DOTALL
        )

        if reason_match:

            reason = reason_match.group(1).strip()

        # ====================================================
        # CLEAN NAME
        # ====================================================

        name = clean_text(name)

        name = re.sub(
            r"\s+(?:SCORE|Score|REASON|Reason)\s*:.*$",
            "",
            name,
            flags=re.IGNORECASE
        )

        name = name.strip()

        # ====================================================
        # CLEAN REASON
        # ====================================================

        reason = clean_text(reason)

        # ====================================================
        # ADD RECOMMENDATION
        # ====================================================

        if name:

            recommendations.append({
                "name": name,
                "score": score,
                "reason": reason
            })

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    unique = []

    seen = set()

    for item in recommendations:

        key = item["name"].lower()

        if key not in seen:

            seen.add(key)

            unique.append(item)

    return unique


# ============================================================
# RANK RECOMMENDATIONS
# ============================================================

def rank_recommendations(recommendations):

    if not recommendations:
        return []

    recommendations = sorted(
        recommendations,
        key=lambda x: int(
            x.get("score", 0)
        ),
        reverse=True
    )

    for index, item in enumerate(
        recommendations,
        start=1
    ):

        item["rank"] = index

    return recommendations


# ============================================================
# DISPLAY RANKING
# ============================================================

def display_ranking(recommendations):

    print("\n" + "=" * 65)

    print(
        "                 RECOMMENDATION RANKING"
    )

    print("=" * 65)

    for item in recommendations:

        print(
            f"\nRank {item.get('rank', '-')}"
        )

        print(
            f"Recommendation : "
            f"{item.get('name', 'Unknown')}"
        )

        print(
            f"Suitability    : "
            f"{item.get('score', 0)}%"
        )

        print(
            f"Reason         : "
            f"{item.get('reason', 'No reason provided.')}"
        )

        print("-" * 65)