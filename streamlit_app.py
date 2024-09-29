import streamlit as st

# Dictionary of chicken recipes
recipes = {
    "Grilled Lemon Chicken": {
        "Ingredients": [
            "4 boneless chicken breasts",
            "1/4 cup olive oil",
            "1/4 cup lemon juice",
            "2 cloves garlic, minced",
            "1 tsp dried oregano",
            "Salt and pepper to taste"
        ],
        "Instructions": [
            "1. In a small bowl, mix olive oil, lemon juice, garlic, oregano, salt, and pepper.",
            "2. Place chicken breasts in a resealable plastic bag and pour marinade over them.",
            "3. Seal the bag and refrigerate for at least 30 minutes.",
            "4. Preheat the grill to medium heat.",
            "5. Grill chicken for 6-7 minutes per side or until fully cooked.",
            "6. Serve hot with your favorite side dish."
        ]
    },
    "Chicken Alfredo": {
        "Ingredients": [
            "2 boneless chicken breasts",
            "1 tbsp olive oil",
            "1 cup heavy cream",
            "1/2 cup Parmesan cheese",
            "2 cloves garlic, minced",
            "Salt and pepper to taste",
            "8 oz fettuccine pasta"
        ],
        "Instructions": [
            "1. Cook pasta according to package directions, then drain.",
            "2. Heat olive oil in a pan over medium heat, season chicken with salt and pepper, and cook until browned and fully cooked.",
            "3. Remove chicken and set aside. In the same pan, add garlic and sauté for 1 minute.",
            "4. Add heavy cream and bring to a simmer, then add Parmesan cheese and stir until melted.",
            "5. Slice the cooked chicken and add it back to the sauce.",
            "6. Toss the sauce with the cooked pasta and serve."
        ]
    },
    "Baked Honey Garlic Chicken": {
        "Ingredients": [
            "4 boneless chicken thighs",
            "1/4 cup honey",
            "3 tbsp soy sauce",
            "2 cloves garlic, minced",
            "1 tbsp olive oil",
            "Salt and pepper to taste"
        ],
        "Instructions": [
            "1. Preheat oven to 375°F (190°C).",
            "2. In a bowl, whisk together honey, soy sauce, garlic, olive oil, salt, and pepper.",
            "3. Place chicken thighs in a baking dish and pour the sauce over them.",
            "4. Bake for 25-30 minutes or until fully cooked.",
            "5. Serve with rice or vegetables."
        ]
    }
}

# Streamlit app interface
st.title("Delicious Chicken Recipes")
st.write("Select a recipe from the dropdown to see its ingredients and instructions.")

# Dropdown to select a recipe
recipe_choice = st.selectbox("Choose a recipe:", list(recipes.keys()))

# Display the selected recipe
if recipe_choice:
    st.header(recipe_choice)
    st.subheader("Ingredients:")
    for ingredient in recipes[recipe_choice]["Ingredients"]:
        st.write(f"- {ingredient}")
    
    st.subheader("Instructions:")
    for instruction in recipes[recipe_choice]["Instructions"]:
        st.write(instruction)

# Option to display the image of chicken if you have URLs or local images
# st.image("path_to_image.jpg", caption=recipe_choice)  # Uncomment and use a path or URL to display an image