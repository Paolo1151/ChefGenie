-- Create Temp Table that calculates the total_calories and applies filters
SELECT
	Y.id,
	Y.name,
	Y.tags,
	SUM(Z.calories * X.required_amount) AS total_calories
INTO
	total_calories_lookup
FROM
    recipe_requirement X
    INNER JOIN recipe_recipe Y ON Y.id = X.recipe_id
    INNER JOIN recipe_ingredient Z ON Z.id = X.ingredient_id
[ingredient_filters]
GROUP BY
	Y.id,
	Y.name,
	Y.tags;

   