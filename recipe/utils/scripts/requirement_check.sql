select
	rr2.name,
	ri.id,
	ri.name,
	(rr.required_amount / rr.required_amount) as amount,
	ri.unit,
	case when ru.ingredient_id is null then 0 else 1 end as pantry_amount,
	((case when ru.ingredient_id is null then 0 else 1 end) - (rr.required_amount / rr.required_amount)) as difference 
from
	recipe_requirement rr
	inner join recipe_recipe rr2 on rr2.id = rr.recipe_id
	inner join recipe_ingredient ri on ri.id = rr.ingredient_id 
	left join recipe_userpantry ru on ru.ingredient_id = ri.id 
where
	rr2.id=[RECIPE_ID]