-- Return filtered id with total_calories
SELECT
	X.id,
	X.name,
	X.tags,
	X.steps 
FROM
    recipe_recipe X
    INNER JOIN total_calories_lookup Y ON Y.id = X.id
[calorie_filter]