# Nutrition
Which nutrients will I be using as constraints and what will I be optimizing?  
Ultimately I would like to be able to optimize for price.  This would require price per unit data, which would likely need to be entered manually as webscraping is currently beyond my abilities.  

For the MVP, I am optimizing to meet nutrient requirements with an objective function of minimizing calories.  
The formulation of this problem is as follows:
1) Data collection: collect food data with comprehensive nutrition label type information.  Also compile nutrition requirement data per the national academies guidelines.
2) Format the data and ensure that the nutrition info corresponds to the nutrition requirements with respect to units
3) Formulate the problem to arrive at a solution using the PuLP package. 

### Repo Organization
The whfoods.ipynb notebook is the current focus of development on the whfoods dataset.  It holds 117 foods with information on macronutrients, micronutrients, and granular macronutrient data on amino acid, fatty acid, and carbohydrate breakdowns.

The data_wrangling.ipynb notebook contains efforts to clean the kaggle Nutrition dataset.  This dataset is less useful than the whfoods data as it is overly granular with regards to food type and also does not include enough fruit, vegetables, and nuts.  Eventually, it will be necessary to incorporate additional foods into the whfoods dataset.

### Further development
1) sustainability: water/energy input requirements for world population nutrition levels.
2) 