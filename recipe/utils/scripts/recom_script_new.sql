SELECT
    *
FROM
    recipe_recipe rr
WHERE
    rr.id not in (
        SELECT DISTINCT
            recipe_id
        from
            recipe_mealmade rm
        where
            rm.user_id = [USERID]
    )