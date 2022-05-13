select distinct
	rr2.*
from
	recipe_requirement rr
	left join recipe_ingredient ri on ri.id = rr.ingredient_id
	left join recipe_recipe rr2 on rr2.id = rr.recipe_id 
where
	ri.category in (
		select
			category
		from
		(
			select
				*,
				RANK() over (order by weighted_count desc) as rank
			from
			(
				select
					ri.category,
					COUNT(ri.category) * rm.amount as weighted_count
				from
					recipe_mealmade rm
					left join recipe_requirement rr on rr.recipe_id = rm.recipe_id 
					left join recipe_ingredient ri on ri.id = rr.ingredient_id
				where
					rm.user_id = 1
					and ri.category not in ('condiment', 'herb', 'miscellaneous')
				group by
					ri.category,
					rm.amount
				order by
					weighted_count desc
			) q
		) r
		where
			r.rank = 1
	)
order by
	rr2.id