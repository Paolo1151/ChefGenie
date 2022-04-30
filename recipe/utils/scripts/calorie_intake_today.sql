SELECT
    m.date,
    SUM(m.total_calories) as calories_per_day
FROM
(
    SELECT 
        x.id,
        x.date,
        x.recipe_id,
        x.user_id,
        SUM(A.calories * Z.required_amount * X.amount) AS total_calories
    FROM 
        recipe_mealmade X
        inner join recipe_recipe Y on X.recipe_id = Y.id
        inner join recipe_requirement Z on Z.recipe_id = Y.id
        inner join recipe_ingredient A on A.id = Z.ingredient_id
    GROUP BY
        x.id,
        x.date,
        x.recipe_id,
        x.user_id
) m
WHERE
    m.user_id = [USERID]
    AND m.date = current_date
GROUP BY
    m.date