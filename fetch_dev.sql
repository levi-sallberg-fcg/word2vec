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

-- select articles from Finansinspektionen
select id, title, description, text
from articles
where publisher_id = '9a6fe83f-ed66-420e-89b8-2c855395afa8'
limit 100;


-- With tags finansinspektionen
select a.id, a.link, a.title, a.description, a.text, coalesce(tags.tags, '[]') as tags
from articles a
left join (
    select ata.article_id, json_agg(at.value) as tags
    from article_tags at
             inner join article_tag_association ata on at.id = ata.tag_id
    where at.value in (
                       'Penningtvätt',
                       'Tjänstepensionsföretag',
                       'Hållbarhet',
                       'Sanktioner',
                       'Försäkringsföretag',
                       'Värdepappersinstitut',
                       'Bank och kredit',
                       'Pensionsstiftelser',
                       'Försäkring',
                       'Bank',
                       'Försäkringsförmedlare'
        )
    group by ata.article_id
) tags on tags.article_id = a.id
where a.text is not null AND a.publisher_id = '9a6fe83f-ed66-420e-89b8-2c855395afa8';


select a.id, a.link, a.title, a.description, a.text
from articles a
where text is not null and a.publisher_id IN (
                                              'da0e66b1-b2f9-4349-9ecd-2868caee58ae',
                                              'f317d418-4e83-43fd-9b07-72aa28a795c3'
    );


