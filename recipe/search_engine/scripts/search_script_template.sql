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
GROUP BY
	Y.id,
	Y.name,
	Y.tags;

-- Query all the recommendations that have the filters. Has default filter based on Search Terms
SELECT
    tcl.id,
    tcl.name,
    tcl.tags
FROM
    total_calories_lookup tcl
    LEFT JOIN recipe_recipereview rr on tcl.id = rr.recipe_id
WHERE
[Filters]

   