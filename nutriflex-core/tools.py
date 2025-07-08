from langchain.tools import Tool
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

# ----- Base Functions ----- #

def nutritional_info_tool(food_description: str) -> str:
    try:
        prompt = f"""
        Provide detailed nutritional information for: {food_description}

        Return the information in this exact format:

        **Food:** {food_description}
        **Calories:** [number] kcal
        **Protein:** [number]g
        **Carbohydrates:** [number]g
        **Fat:** [number]g
        **Fiber:** [number]g
        **Sugar:** [number]g
        **Sodium:** [number]mg

        Be as accurate as possible using standard nutritional databases.
        """
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error retrieving nutritional information: {str(e)}"

def calculate_tdee(age: int, weight: float, height: float, gender: str, activity_level: str, goal: str) -> str:
    weight_kg = weight * 0.453592
    height_cm = height * 2.54
    if gender.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    activity_multipliers = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725
    }
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)

    if goal == "lose_weight":
        target_calories = tdee - 500
    elif goal == "gain_weight":
        target_calories = tdee + 500
    else:
        target_calories = tdee

    protein_g = (target_calories * 0.30) / 4
    carbs_g = (target_calories * 0.40) / 4
    fat_g = (target_calories * 0.30) / 9

    return f"""
    **Daily Targets:**
    - **Calories:** {target_calories:.0f} kcal
    - **Protein:** {protein_g:.0f}g
    - **Carbohydrates:** {carbs_g:.0f}g
    - **Fat:** {fat_g:.0f}g

    **Calculated BMR:** {bmr:.0f} kcal
    **Calculated TDEE:** {tdee:.0f} kcal
    **Goal Adjustment:** {goal.replace('_', ' ').title()}
    """

# ----- LangChain-Compatible Tools ----- #

nutritional_info_tool = Tool(
    name="Nutritional Info",
    func=nutritional_info_tool,
    description="Provides detailed nutritional information about a food item."
)

tdee_tool = Tool(
    name="TDEE Calculator",
    func=calculate_tdee,
    description="Calculates total daily energy expenditure and macro targets."
)