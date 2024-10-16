SELECT 
	u.id, 
	u.email, 
	COUNT(l.id) AS count_links,
	SUM(CASE WHEN l.link_type = 'website' THEN 1 ELSE 0 END) AS website,
	SUM(CASE WHEN l.link_type = 'book' THEN 1 ELSE 0 END) AS book,
	SUM(CASE WHEN l.link_type = 'article' THEN 1 ELSE 0 END) AS article,
	SUM(CASE WHEN l.link_type = 'music' THEN 1 ELSE 0 END) AS music,
	SUM(CASE WHEN l.link_type = 'video' THEN 1 ELSE 0 END) AS video
FROM public.users_useraccount u
JOIN public.links_link l ON u.id = l.user_id
GROUP BY u.id
ORDER BY COUNT(l.id) DESC, u.created_at ASC
LIMIT 10;