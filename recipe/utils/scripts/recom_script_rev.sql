select
	q.id,
	q.tags
from
(
	select
		rr2.id,
		rr2.tags,
		RANK() over (order by rr.rating desc, rr.created_at)
	from
		recipe_recipereview rr
		left join recipe_recipe rr2 on rr2.id = rr.recipe_id
	where
		rr.user_id = [USERID]
) q
where
	q.rank <= 3