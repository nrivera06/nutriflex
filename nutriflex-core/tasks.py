from crewai import Task

def create_discovery_task(user_input: str):
    """Create the initial diet discovery task"""
    return Task(
        description=f"""
        Analyze the user profile and create a comprehensive diet strategy comparison.
        
        User Input: {user_input}
        
        Your task:
        1. Extract key information: age, weight, height, gender, activity level, and goals
        2. Calculate the user's TDEE and daily nutritional targets
        3. Present 3 distinct dietary strategies:
           - Mediterranean Diet
           - Low-Carb Diet  
           - Balanced Macro Diet
        
        For each strategy, provide:
        - Core principles and food focus
        - Pros and cons specific to this user
        - Sample day of meals
        - Expected timeline for results
        
        Format your response in clear markdown with headers and bullet points.
        Include the calculated daily targets at the beginning.
        """,
        expected_output="A comprehensive markdown report comparing 3 diet strategies with calculated nutritional targets"
    )

def create_budget_task():
    """Create the budget analysis task"""
    return Task(
        description="""
        Create detailed budget breakdowns for the recommended dietary strategies.
        
        For each of the 3 diet strategies mentioned in the previous analysis:
        1. Create sample one-day menus for 3 budget levels:
           - Thrifty (<$15/day)
           - Standard (<$25/day) 
           - Premium (<$40/day)
        
        2. For each budget level, provide:
           - Complete breakfast, lunch, dinner, and snack
           - Estimated cost breakdown by meal
           - Smart shopping tips for that budget tier
           - Ingredient substitutions between tiers
        
        3. Highlight the key differences in ingredient quality and variety between budget levels
        
        Format as markdown with clear sections for each diet strategy and budget tier.
        """,
        expected_output="Detailed budget analysis with sample menus for each diet strategy across 3 price tiers"
    )

def create_meal_adjustment_task(daily_targets: str, meal_logged: str, previous_meals: str = ""):
    """Create real-time meal adjustment task"""
    return Task(
        description=f"""
        Provide tactical meal adjustment based on current nutritional intake.
        
        **Daily Targets:** {daily_targets}
        **Meal Just Eaten:** {meal_logged}
        **Previous Meals Today:** {previous_meals}
        
        Your task:
        1. Look up the nutritional information for the meal just eaten
        2. Calculate the remaining nutritional budget for the day
        3. Generate a specific recipe for the next meal that:
           - Fits within the remaining calorie budget
           - Balances the macronutrients appropriately
           - Is realistic and appealing
        
        4. Provide the recipe with:
           - Ingredient list with quantities
           - Simple cooking instructions
           - Estimated prep/cook time
           - Nutritional breakdown
        
        5. Include tips for staying on track for the rest of the day
        
        Be precise with numbers and practical with recommendations.
        """,
        expected_output="A specific meal recipe with nutritional breakdown that fits the remaining daily budget"
    )

def create_cheat_mode_task(cheat_request: str, daily_targets: str):
    """Create cheat mode strategy task"""
    return Task(
        description=f"""
        Design a "Cheat Mode" strategy for the user's indulgence request.
        
        **Cheat Request:** {cheat_request}
        **Daily Targets:** {daily_targets}
        
        Your task:
        1. Estimate the caloric impact of the requested cheat meal
        2. Create a "Calorie Banking" strategy:
           - Calculate the excess calories
           - Spread the deficit across 2-3 days before/after
           - Ensure the daily deficit doesn't exceed 300-400 calories
        
        3. Provide specific meal plans for the "banking" days:
           - Lower-calorie but satisfying meals
           - Maintain adequate protein and nutrients
           - Include meal timing suggestions
        
        4. Give the user a clear day-by-day plan showing:
           - Modified calorie targets for each day
           - Specific meal suggestions
           - How this maintains their weekly average
        
        5. Include motivational messaging about balance and sustainability
        
        Make this feel like a strategic plan, not a restriction.
        """,
        expected_output="A comprehensive cheat mode strategy with day-by-day meal plans and calorie banking"
    )