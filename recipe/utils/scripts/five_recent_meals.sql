SELECT
    m.date,
    m.name,
    m.total_calories
FROM
(
    SELECT 
        x.id,
        x.date,
        x.recipe_id,
        x.user_id,
        SUM(A.calories * Z.required_amount * X.amount) AS total_calories,
        y.name
    FROM 
        recipe_mealmade X
        inner join recipe_recipe Y on X.recipe_id = Y.id
        inner join recipe_requirement Z on Z.recipe_id = Y.id
        inner join recipe_ingredient A on A.id = Z.ingredient_id
    GROUP BY
        x.id,
        x.date,
        x.recipe_id,
        x.user_id,
        y.name
) m
WHERE
    m.user_id = [USERID]
GROUP BY
    m.date,
    m.total_calories,
    m.name
ORDER BY
    m.date DESC
LIMIT 
    5