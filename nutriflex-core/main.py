from crewai import Crew, Process
from agents import nico, lucas, joaquin, nathaniel
from tasks import (
    create_discovery_task, 
    create_budget_task, 
    create_meal_adjustment_task,
    create_cheat_mode_task
)
import os
from dotenv import load_dotenv

load_dotenv()

class NutriFlexCrew:
    """Main class to orchestrate different crew workflows"""
    
    def __init__(self):
        self.setup_environment()
    
    def setup_environment(self):
        """Setup environment variables"""
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    def run_onboarding_crew(self, user_input: str):
        """Run the complete onboarding process with diet discovery and budget analysis"""
        
        # Create tasks
        discovery_task = create_discovery_task(user_input)
        budget_task = create_budget_task()
        
        # Assign agents to tasks
        discovery_task.agent = lucas
        budget_task.agent = joaquin
        
        # Create sequential task dependency
        budget_task.context = [discovery_task]
        
        # Create crew
        crew = Crew(
            agents=[lucas, joaquin],
            tasks=[discovery_task, budget_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute crew
        result = crew.kickoff()
        return result
    
    def run_meal_adjustment_crew(self, daily_targets: str, meal_logged: str, previous_meals: str = ""):
        """Run real-time meal adjustment"""
        
        # Create task
        adjustment_task = create_meal_adjustment_task(daily_targets, meal_logged, previous_meals)
        adjustment_task.agent = nathaniel
        
        # Create crew
        crew = Crew(
            agents=[nathaniel],
            tasks=[adjustment_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute crew
        result = crew.kickoff()
        return result
    
    def run_cheat_mode_crew(self, cheat_request: str, daily_targets: str):
        """Run cheat mode strategy creation"""
        
        # Create task
        cheat_task = create_cheat_mode_task(cheat_request, daily_targets)
        cheat_task.agent = lucas
        
        # Create crew
        crew = Crew(
            agents=[lucas],
            tasks=[cheat_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute crew
        result = crew.kickoff()
        return result

# Convenience functions for direct use
def run_onboarding(user_input: str):
    """Convenience function to run onboarding workflow"""
    crew_manager = NutriFlexCrew()
    return crew_manager.run_onboarding_crew(user_input)

def run_meal_adjustment(daily_targets: str, meal_logged: str, previous_meals: str = ""):
    """Convenience function to run meal adjustment workflow"""
    crew_manager = NutriFlexCrew()
    return crew_manager.run_meal_adjustment_crew(daily_targets, meal_logged, previous_meals)

def run_cheat_mode(cheat_request: str, daily_targets: str):
    """Convenience function to run cheat mode workflow"""
    crew_manager = NutriFlexCrew()
    return crew_manager.run_cheat_mode_crew(cheat_request, daily_targets)

if __name__ == "__main__":
    # Test the system
    test_input = "I'm a 30-year-old male, 180 lbs, 6 feet tall, moderately active, and I want to lose weight"
    
    print("Testing Onboarding Crew...")
    result = run_onboarding(test_input)
    print(result)
    
    print("\n" + "="*50 + "\n")
    
    print("Testing Meal Adjustment Crew...")
    targets = "Daily Targets: 1900 calories, 150g protein, 190g carbs, 63g fat"
    meal = "I had a McDonald's Big Mac meal with large fries and a Coke"
    result = run_meal_adjustment(targets, meal)
    print(result)