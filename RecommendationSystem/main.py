from input_module import (
    collect_user_profile,
    display_profile
)

from profile_module import (
    analyze_profile,
    display_analysis
)

from prompt_module import (
    construct_prompt,
    display_prompt
)

from recommendation_module import (
    generate_recommendations
)

from ranking_module import (
    extract_recommendations,
    rank_recommendations,
    display_ranking
)

from explanation_module import (
    display_explanations
)

from feedback_module import (
    collect_feedback,
    create_refinement_prompt
)

from intent_module import (
    detect_intent
)

from save_module import (
    save_recommendations
)


# ============================================================
# GENERATE INITIAL RECOMMENDATIONS
# ============================================================

def generate_initial_recommendations(profile, analysis):

    prompt = construct_prompt(
        profile,
        analysis
    )

    # Display prompt for Part C
    display_prompt(prompt)

    print("\n" + "=" * 65)
    print("          GENERATING RECOMMENDATIONS...")
    print("=" * 65)

    response = generate_recommendations(
        prompt
    )

    if not response:

        print(
            "\nCould not generate recommendations."
        )

        return []

    # Display GPT/Ollama response
    print("\nGPT RESPONSE")
    print("-" * 65)
    print(response)

    # Extract recommendations
    recommendations = extract_recommendations(
        response
    )

    if not recommendations:

        print(
            "\nCould not process the GPT response."
        )

        return []

    # Rank recommendations
    recommendations = rank_recommendations(
        recommendations
    )

    # Display ranking
    display_ranking(
        recommendations
    )

    # Display explanations
    display_explanations(
        recommendations
    )

    return recommendations


# ============================================================
# REFINE RECOMMENDATIONS
# ============================================================

def refine_recommendations(
    profile,
    recommendations,
    feedback
):

    prompt = create_refinement_prompt(
        profile,
        recommendations,
        feedback
    )

    print("\n" + "=" * 65)
    print("             REFINING RECOMMENDATIONS")
    print("=" * 65)

    response = generate_recommendations(
        prompt
    )

    if not response:

        print(
            "\nCould not generate refined recommendations."
        )

        return recommendations

    print("\nREFINED GPT RESPONSE")
    print("-" * 65)
    print(response)

    # Extract refined recommendations
    refined = extract_recommendations(
        response
    )

    if not refined:

        print(
            "\nCould not process refined recommendations."
        )

        return recommendations

    # Rank refined recommendations
    refined = rank_recommendations(
        refined
    )

    # Display ranking
    display_ranking(
        refined
    )

    # Display explanations
    display_explanations(
        refined
    )

    return refined


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    # ========================================================
    # PART A - USER PROFILE COLLECTION
    # ========================================================

    profile = collect_user_profile()

    # ========================================================
    # DISPLAY USER PROFILE
    # ========================================================

    display_profile(
        profile
    )

    # ========================================================
    # PART B - PREFERENCE ANALYSIS
    # ========================================================

    analysis = analyze_profile(
        profile
    )

    display_analysis(
        analysis
    )

    # ========================================================
    # PART C, D, E, F
    # INITIAL RECOMMENDATIONS
    # ========================================================

    recommendations = generate_initial_recommendations(
        profile,
        analysis
    )

    if not recommendations:

        print(
            "\nNo recommendations generated."
        )

        return

    # ========================================================
    # PART G, H, I
    # CONTINUOUS INTERACTION
    # ========================================================

    while True:

        print("\n" + "=" * 65)
        print(
            "             ASSISTANT MENU"
        )
        print("=" * 65)

        print(
            "1. Generate Recommendation"
        )

        print(
            "2. Refine Recommendation"
        )

        print(
            "3. Show Profile"
        )

        print(
            "4. Explain Recommendation"
        )

        print(
            "5. Save Recommendation"
        )

        print(
            "6. Exit"
        )

        user_input = input(
            "\nEnter your request or command: "
        ).strip()

        # ====================================================
        # EMPTY INPUT
        # ====================================================

        if not user_input:

            print(
                "\nPlease enter a command."
            )

            continue

        # ====================================================
        # INTENT DETECTION
        # ====================================================
        #
        # Menu numbers are detected directly.
        # This avoids an unnecessary Ollama call.
        #
        # Natural language commands are sent to Ollama.
        # ====================================================

        if user_input == "1":

            intent = "GENERATE_RECOMMENDATION"

        elif user_input == "2":

            intent = "REFINE_RECOMMENDATION"

        elif user_input == "3":

            intent = "SHOW_PROFILE"

        elif user_input == "4":

            intent = "EXPLAIN_RECOMMENDATION"

        elif user_input == "5":

            intent = "SAVE_RECOMMENDATION"

        elif user_input == "6":

            intent = "EXIT"

        else:

            # Only natural-language requests
            # use AI intent detection.

            try:

                intent = detect_intent(
                    user_input
                )

            except Exception as error:

                print(
                    f"\nIntent detection error: {error}"
                )

                continue

        print(
            f"\nDetected Intent: {intent}"
        )

        # ====================================================
        # GENERATE RECOMMENDATION
        # ====================================================

        if intent == "GENERATE_RECOMMENDATION":

            new_recommendations = (
                generate_initial_recommendations(
                    profile,
                    analysis
                )
            )

            if new_recommendations:

                recommendations = (
                    new_recommendations
                )

        # ====================================================
        # REFINE RECOMMENDATION
        # ====================================================

        elif intent == "REFINE_RECOMMENDATION":

            # If user entered "2", ask for actual feedback.

            if user_input == "2":

                feedback = collect_feedback()

            else:

                # Natural-language feedback
                feedback = user_input

            recommendations = (
                refine_recommendations(
                    profile,
                    recommendations,
                    feedback
                )
            )

        # ====================================================
        # SHOW PROFILE
        # ====================================================

        elif intent == "SHOW_PROFILE":

            display_profile(
                profile
            )

            display_analysis(
                analysis
            )

        # ====================================================
        # EXPLAIN RECOMMENDATION
        # ====================================================

        elif intent == "EXPLAIN_RECOMMENDATION":

            display_explanations(
                recommendations
            )

        # ====================================================
        # SAVE RECOMMENDATION
        # ====================================================

        elif intent == "SAVE_RECOMMENDATION":

            save_recommendations(
                recommendations
            )

        # ====================================================
        # EXIT
        # ====================================================

        elif intent == "EXIT":

            print("\n" + "=" * 65)

            print(
                "Thank you for using the "
                "Personalized Recommendation System!"
            )

            print("=" * 65)

            break

        # ====================================================
        # UNKNOWN INTENT
        # ====================================================

        else:

            print(
                "\nUnable to determine the requested action."
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()