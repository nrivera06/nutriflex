import streamlit as st
import re
from main import run_onboarding, run_meal_adjustment, run_cheat_mode
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="NutriFlex AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #4CAF50;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e7f3ff;
        border: 1px solid #b8daff;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'onboarding_complete' not in st.session_state:
    st.session_state.onboarding_complete = False
if 'daily_targets' not in st.session_state:
    st.session_state.daily_targets = ""
if 'meal_log' not in st.session_state:
    st.session_state.meal_log = []
if 'current_strategy' not in st.session_state:
    st.session_state.current_strategy = ""

# Main title
st.markdown('<div class="main-header">🥗 NutriFlex AI</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Your Personal AI Nutrition Crew</div>', unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox(
    "Choose your workflow:",
    ["🚀 Get Started", "⚡ Meal Adjustment", "🎉 Cheat Mode", "📊 My Progress"]
)

# Sidebar info
if st.session_state.onboarding_complete:
    st.sidebar.markdown("### Your Current Plan")
    st.sidebar.info(f"Strategy: {st.session_state.current_strategy}")
    st.sidebar.markdown("### Today's Meals")
    for i, meal in enumerate(st.session_state.meal_log, 1):
        st.sidebar.text(f"{i}. {meal[:30]}...")

# Main content area
if app_mode == "🚀 Get Started":
    st.markdown('<div class="subheader">Welcome to NutriFlex AI!</div>', unsafe_allow_html=True)
    
    if not st.session_state.onboarding_complete:
        st.markdown("""
        Our AI nutrition crew is ready to create your personalized meal plan! 
        
        **Meet your team:**
        - 🧑‍💼 **Alex** - Your Personal Concierge
        - 👩‍⚕️ **Dr. Evelyn Reed** - Diet Architect & Nutritionist  
        - 💰 **Budget Ben** - Financial Meal Planning Analyst
        - ⚡ **Kai** - Tactical Meal Adjuster
        """)
        
        st.markdown("### Tell us about yourself:")
        
        # User input form
        with st.form("user_profile"):
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("Age", min_value=18, max_value=100, value=30)
                weight = st.number_input("Weight (lbs)", min_value=80, max_value=400, value=180)
                height = st.number_input("Height (inches)", min_value=48, max_value=84, value=70)
            
            with col2:
                gender = st.selectbox("Gender", ["Male", "Female"])
                activity = st.selectbox("Activity Level", 
                    ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
                goal = st.selectbox("Primary Goal", 
                    ["Lose Weight", "Maintain Weight", "Gain Weight"])
            
            additional_info = st.text_area(
                "Additional Information (dietary restrictions, preferences, etc.)",
                placeholder="e.g., vegetarian, gluten-free, loves Mediterranean food..."
            )
            
            submitted = st.form_submit_button("🚀 Create My Nutrition Plan")
        
        if submitted:
            # Create user profile string
            user_input = f"""
            User Profile:
            - Age: {age} years old
            - Weight: {weight} lbs
            - Height: {height} inches
            - Gender: {gender}
            - Activity Level: {activity}
            - Goal: {goal}
            - Additional Info: {additional_info if additional_info else 'None'}
            """
            
            # Show loading spinner
            with st.spinner("🤖 Your AI nutrition crew is working on your personalized plan..."):
                try:
                    # Run the onboarding crew
                    result = run_onboarding(user_input)
                    
                    # Save to session state
                    st.session_state.onboarding_complete = True
                    st.session_state.current_strategy = "Custom Plan"
                    
                    # Extract daily targets if possible
                    if "Daily Targets:" in str(result):
                        lines = str(result).split('\n')
                        target_lines = [line for line in lines if 'Calories:' in line or 'Protein:' in line or 'Carbohydrates:' in line or 'Fat:' in line]
                        st.session_state.daily_targets = '\n'.join(target_lines)
                    
                    # Display results
                    st.success("🎉 Your personalized nutrition plan is ready!")
                    st.markdown(result)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.error("Please check your API key and try again.")
    
    else:
        st.success("✅ Your nutrition plan is ready! Use the sidebar to navigate to other features.")
        st.markdown("### Your Plan Overview")
        st.info("Your personalized nutrition plan has been created. You can now:")
        st.markdown("""
        - ⚡ **Log meals** and get real-time adjustments
        - 🎉 **Enable Cheat Mode** for planned indulgences
        - 📊 **Track your progress** throughout the day
        """)

elif app_mode == "⚡ Meal Adjustment":
    st.markdown('<div class="subheader">Real-Time Meal Adjustment</div>', unsafe_allow_html=True)
    
    if not st.session_state.onboarding_complete:
        st.warning("⚠️ Please complete the onboarding process first!")
        st.stop()
    
    st.markdown("**Kai, your Tactical Meal Adjuster, is ready to help!**")
    
    # Meal logging form
    with st.form("meal_log"):
        st.markdown("### Log a meal you just ate:")
        meal_description = st.text_input(
            "Describe your meal:",
            placeholder="e.g., 'I had a chicken Caesar salad with dressing and croutons'"
        )
        
        log_meal = st.form_submit_button("🍽️ Log Meal & Get Adjustment")
    
    if log_meal and meal_description:
        # Add to meal log
        st.session_state.meal_log.append(f"{datetime.now().strftime('%H:%M')} - {meal_description}")
        
        # Show loading spinner
        with st.spinner("⚡ Kai is calculating your meal adjustment..."):
            try:
                # Prepare previous meals context
                previous_meals = "\n".join(st.session_state.meal_log[:-1]) if len(st.session_state.meal_log) > 1 else "No previous meals today"
                
                # Run meal adjustment
                result = run_meal_adjustment(
                    st.session_state.daily_targets,
                    meal_description,
                    previous_meals
                )
                
                # Display results
                st.success("✅ Meal logged successfully!")
                st.markdown("### Your Recommended Next Meal:")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    # Display current meal log
    if st.session_state.meal_log:
        st.markdown("### Today's Meal Log:")
        for meal in st.session_state.meal_log:
            st.text(f"• {meal}")

elif app_mode == "🎉 Cheat Mode":
    st.markdown('<div class="subheader">Cheat Mode Strategy</div>', unsafe_allow_html=True)
    
    if not st.session_state.onboarding_complete:
        st.warning("⚠️ Please complete the onboarding process first!")
        st.stop()
    
    st.markdown("**Dr. Evelyn Reed will create a strategic plan for your indulgence!**")
    
    st.info("""
    🎯 **How Cheat Mode Works:**
    Our AI will create a "calorie banking" strategy that allows you to enjoy your favorite foods 
    while staying on track with your weekly goals. You'll get specific meal plans for the days 
    before and after to balance out the indulgence.
    """)
    
    # Cheat mode form
    with st.form("cheat_mode"):
        st.markdown("### What would you like to indulge in?")
        
        col1, col2 = st.columns(2)
        with col1:
            cheat_food = st.text_input(
                "Describe your desired cheat meal:",
                placeholder="e.g., 'Large pepperoni pizza and beer'"
            )
        with col2:
            cheat_day = st.selectbox(
                "When do you want to indulge?",
                ["Today", "Tomorrow", "This Weekend", "Next Week"]
            )
        
        cheat_context = st.text_area(
            "Any additional context?",
            placeholder="e.g., 'Birthday dinner', 'Date night', 'Celebrating achievement'..."
        )
        
        activate_cheat = st.form_submit_button("🎉 Activate Cheat Mode")
    
    if activate_cheat and cheat_food:
        cheat_request = f"I want to have {cheat_food} on {cheat_day}. Context: {cheat_context}"
        
        # Show loading spinner
        with st.spinner("🎉 Dr. Evelyn Reed is designing your cheat mode strategy..."):
            try:
                # Run cheat mode crew
                result = run_cheat_mode(cheat_request, st.session_state.daily_targets)
                
                # Display results
                st.success("🎉 Cheat Mode Activated!")
                st.markdown("### Your Strategic Indulgence Plan:")
                st.markdown(result)
                
                st.balloons()  # Celebration animation
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

elif app_mode == "📊 My Progress":
    st.markdown('<div class="subheader">Progress Tracking</div>', unsafe_allow_html=True)
    
    if not st.session_state.onboarding_complete:
        st.warning("⚠️ Please complete the onboarding process first!")
        st.stop()
    
    st.markdown("### Today's Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Meals Logged", len(st.session_state.meal_log))
    
    with col2:
        st.metric("Days Active", "1")  # Placeholder
    
    with col3:
        st.metric("Plan Adherence", "85%")  # Placeholder
    
    # Display targets
    if st.session_state.daily_targets:
        st.markdown("### Your Daily Targets:")
        st.code(st.session_state.daily_targets)
    
    # Display meal history
    if st.session_state.meal_log:
        st.markdown("### Meal History:")
        for i, meal in enumerate(st.session_state.meal_log, 1):
            st.markdown(f"**{i}.** {meal}")
    else:
        st.info("No meals logged yet today. Head to the Meal Adjustment section to start tracking!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    Powered by NutriFlex AI Crew • Built with CrewAI & Streamlit
</div>
""", unsafe_allow_html=True)