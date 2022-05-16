SELECT
    m.category,
    count(m.category) as count
FROM
(
    SELECT 
        x.id,
        x.date,
        x.recipe_id,
        x.user_id,
        A.category
    FROM 
        recipe_mealmade X
        inner join recipe_recipe Y on X.recipe_id = Y.id
        inner join recipe_requirement Z on Z.recipe_id = Y.id
        inner join recipe_ingredient A on A.id = Z.ingredient_id
    WHERE 
        x.date >= current_date -7
    GROUP BY
        x.id,
        x.date,
        x.recipe_id,
        x.user_id,
        A.category
) m
WHERE
    m.user_id = [USERID]
    
GROUP BY
    m.category
ORDER BY
    m.category