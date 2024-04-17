# def adjust_feeding_plan(weight, ideal_weight, is_overweight):
#     # Define a daily calorie reduction or increase step for weight management
#     calorie_adjustment_step = 50  # This can be adjusted based on the dog's specific needs
#     exercise_minutes_adjustment = 10  # Increase or decrease daily exercise by this amount

#     # Define the basic feeding and exercise plan
#     plan = {
#         "calorie_adjustment": 0,
#         "exercise_minutes": 30,  # Starting point for daily exercise in minutes
#     }

#     # Adjust feeding and exercise plan based on weight status
#     if is_overweight:
#         # If overweight, reduce daily calorie intake and increase exercise
#         plan["calorie_adjustment"] = -calorie_adjustment_step
#         plan["exercise_minutes"] += exercise_minutes_adjustment
#     else:
#         # If underweight, increase daily calorie intake and adjust exercise as needed
#         plan["calorie_adjustment"] = calorie_adjustment_step
#         # Exercise might be adjusted down for underweight dogs, depending on vet advice
#         # plan["exercise_minutes"] -= exercise_minutes_adjustment

#     # Generate a simple text plan for the next 6 months
#     text_plan = f"To {'reduce' if is_overweight else 'increase'} your dog's weight to an ideal range of {ideal_weight[0]}-{ideal_weight[1]} lbs, adjust its daily calorie intake by {plan['calorie_adjustment']} calories and aim for {plan['exercise_minutes']} minutes of exercise daily. Monitor weight monthly and adjust as necessary."
    
#     return text_plan

# # Modify the suggest_diet_plan function to include the feeding plan
# def suggest_diet_plan_with_feeding(weight, age):
#     # Definitions from the previous function here...
#      ideal_weight = {
#         (0, 1): (0.5, 1.5),
#         (1, 2): (3, 5),
#         (2, 3): (10, 15),
#         (3, 4): (20, 30),
#         (4, 5): (25, 40),
#         (5, 6): (30, 45),
#         (6, 7): (40, 55),
#         (7, 8): (50, 60),
#         (8, 9): (50, 65),
#         (9, 10): (55, 70),
#         (10, 11): (55, 70),
#         (11, 12): (60, 75),
#         (12, 24): (65, 80), # Approximating for 2 years and beyond
#         (24, 36): (70, 85),
#         (36, 48): (75, 90),
#         (48, 60): (75, 90),
#         (60, 72): (75, 90),
#         (72, 84): (70, 85),
#         (84, 96): (65, 80),
#         (96, 108): (65, 80),
#         (108, 120): (60, 75),
#         (120, 132): (60, 75),
#         (132, 144): (55, 70),
#     }
#      if age > 12:
#          age = age * 12

#         # Find the ideal weight range for the dog's age
#      for age_range, weight_range in ideal_weight.items():
#         if age_range[0] <= age <= age_range[1]:
#             min_ideal_weight, max_ideal_weight = weight_range
#             break
#         else:
#             return "Age out of range. Please enter an age between 0 and 12 years."

#     # Check if the dog is overweight
#      if weight > max_ideal_weight:
#         # Suggest a diet plan
#         return f"Your dog is overweight. Aim to gradually reduce its weight to within {min_ideal_weight}-{max_ideal_weight} lbs range by adjusting its diet. Consult a vet for a personalized diet plan."
#      elif weight < min_ideal_weight:
#         return f"Your dog is underweight. Aim to gradually increase its weight to within {min_ideal_weight}-{max_ideal_weight} lbs range by adjusting its diet. Consult a vet for a personalized diet plan."
#      else:
#         return "Your dog's weight is within the ideal range for its age."

#     # Check if the dog is overweight or underweight and suggest a plan
#      if weight > max_ideal_weight:
#         is_overweight = True
#         diet_plan = adjust_feeding_plan(weight, (min_ideal_weight, max_ideal_weight), is_overweight)
#         return f"Your dog is overweight. " + diet_plan
#      elif weight < min_ideal_weight:
#         is_overweight = False
#         diet_plan = adjust_feeding_plan(weight, (min_ideal_weight, max_ideal_weight), is_overweight)
#         return f"Your dog is underweight. " + diet_plan
#      else:
#         return "Your dog's weight is within the ideal range for its age."

# # Example usage
# weight = float(input("Enter your dog's weight in lbs: "))
# age = float(input("Enter your dog's age in months or years: "))
# print(suggest_diet_plan_with_feeding(weight, age))

def adjust_feeding_plan(weight, ideal_weight, is_overweight):
    calorie_adjustment_step = 50
    exercise_minutes_adjustment = 10

    plan = {
        "calorie_adjustment": -calorie_adjustment_step if is_overweight else calorie_adjustment_step,
        "exercise_minutes": 30 + (exercise_minutes_adjustment if is_overweight else -exercise_minutes_adjustment),
    }

    adjustment_direction = "reduce" if is_overweight else "increase"
    text_plan = f"To {adjustment_direction} your dog's weight to an ideal range of {ideal_weight[0]}-{ideal_weight[1]} lbs, " \
                f"adjust its daily calorie intake by {plan['calorie_adjustment']} calories and aim for {plan['exercise_minutes']} minutes of exercise daily. " \
                "Monitor weight monthly and adjust as necessary."

    return text_plan

def suggest_diet_plan_with_feeding(weight, age):
    # Ideal weight ranges for Labrador Retrievers based on age (in months)
    ideal_weight = {
        (0, 2): (5, 10),
        (2, 4): (10, 20),
        (4, 6): (20, 30),
        (6, 12): (30, 40),
        (12, 24): (40, 60),
        (24, 36): (50, 70),
        (36, 48): (60, 80),
        (48, 60): (70, 90),
        (60, 72): (80, 100),
    }

    # Convert age to months if given in years
    if age > 12:
        age *= 12

    min_ideal_weight, max_ideal_weight = (0, 0)
    for age_range, weight_range in ideal_weight.items():
        if age_range[0] <= age <= age_range[1]:
            min_ideal_weight, max_ideal_weight = weight_range
            break

    if min_ideal_weight == 0:
        return "Age out of range. Please enter an age between 0 and 6 years."

    if weight > max_ideal_weight:
        return "Your dog is overweight. " + adjust_feeding_plan(weight, (min_ideal_weight, max_ideal_weight), True)
    elif weight < min_ideal_weight:
        return "Your dog is underweight. " + adjust_feeding_plan(weight, (min_ideal_weight, max_ideal_weight), False)
    else:
        return "Your dog's weight is within the ideal range for its age."

# Interactive part
try:
    weight = float(input("Enter your dog's weight in lbs: "))
    age = float(input("Enter your dog's age in months or years: "))
    print(suggest_diet_plan_with_feeding(weight, age))
except ValueError:
    print("Please enter numeric values for weight and age.")
