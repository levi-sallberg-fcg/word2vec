-- select articles from FCA
select id, title, description, text
from articles
where publisher_id = '45145bda-f7e8-48a7-a9a3-934e3d2c944f'
limit 500;

-- select articles based on regions
select a.id, a.title, a.description
from articles a
inner join publishers p on a.publisher_id = p.id
inner join regions r on p.region_id = r.id
where r.name ilike 'british' or r.name ilike 'european' or r.name ilike 'international';