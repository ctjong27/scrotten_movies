-- SQLite
select count(member_id) as count, member_id, movie_id
from scrotten_movie_to_member_scrottenmovietomember
group by member_id
having count(member_id) > 1


-- select *
-- from scrotten_movie_to_member_scrottenmovietomember s
-- where s.member_id = '/celebrity/1040476-jerry_adler'


-- select *
-- from scrotten_movie_to_member_scrottenmovietomember
-- where movie_id in ('/m/driveways', '/m/a_most_violent_year')


-- select movie_id || ',' || group_concat(member_id, ',')
-- from scrotten_movie_to_member_scrottenmovietomember
-- where movie_id in ('/m/driveways', '/m/a_most_violent_year')
-- group by movie_id


select ''''||movie_id || ',' || member_id||''','
from scrotten_movie_to_member_scrottenmovietomember


select *
from scrotten_movie_to_member_scrottenmovietomember



-- select count(member_id), member_id
-- from scrotten_movie_to_member_scrottenmovietomember
-- where movie_id in ('/m/driveways', '/m/a_most_violent_year')
-- group by member_id