# TODO: Read in data from tv_shows_top_25_yearly.csv
# TODO: Export data into tv_export_data.csv

join data from
tv_cast_image_race_gender.csv
id,name,profile_path,profile_race,profile_gender
1,George Lucas,/WCSZzWdtPmdRxH9LUCVi2JPCSJ.jpg,white,Undetermined
2,Mark Hamill,/2ZulC2Ccq1yv3pemusks6Zlfy2s.jpg,latino hispanic,Male
3,Harrison Ford,/ActhM39LTxgx3tnJv3s5nM6hGD1.jpg,white,Male
4,Carrie Fisher,/utKPqWm9MAcL6NqN0Kd71dWUmXM.jpg,white,Female
6,Anthony Daniels,/7kR4kwXtvXtvrsxWeX3QLX5NS5V.jpg,white,Male
11,David Reynolds,/5iKtATPbLpv2lT7q9DPX2v2qPS1.jpg,white,Male

tv_show_cast_details.csv
id,imdb_id,name,gender,birthday,deathday,profile_path
1,nm0000184,George Lucas,2,1944-05-14,,/WCSZzWdtPmdRxH9LUCVi2JPCSJ.jpg
2,nm0000434,Mark Hamill,2,1951-09-25,,/2ZulC2Ccq1yv3pemusks6Zlfy2s.jpg
3,nm0000148,Harrison Ford,2,1942-07-13,,/ActhM39LTxgx3tnJv3s5nM6hGD1.jpg
4,nm0000402,Carrie Fisher,1,1956-10-21,2016-12-27,/utKPqWm9MAcL6NqN0Kd71dWUmXM.jpg
6,nm0000355,Anthony Daniels,2,1946-02-21,,/7kR4kwXtvXtvrsxWeX3QLX5NS5V.jpg
11,nm0721675,David Reynolds,2,1966-08-10,,/5iKtATPbLpv2lT7q9DPX2v2qPS1.jpg
12,nm1071252,Alexander Gould,2,1994-05-04,,/fe4mUSp0XotA6Ku4Bs69Q9o2lqU.jpg

tv_show_season_to_cast.csv
show_id,season_number,cast_id,cast_name,episode_count,known_for_department,season_air_date
734,1,15112,Tom Selleck,18,Acting,1980-12-11
734,1,12296,John Hillerman,18,Acting,1980-12-11
734,1,42156,Roger E. Mosley,18,Acting,1980-12-11
734,1,159648,Larry Manetti,18,Acting,1980-12-11
734,1,1219196,Jeff MacKay,5,Acting,1980-12-11
734,1,6839,Fritz Weaver,2,Acting,1980-12-11
734,1,151423,Pamela Susan Shoop,2,Acting,1980-12-11
734,1,2249,Clyde Kusatsu,2,Acting,1980-12-11
734,1,1162,Robert Loggia,2,Acting,1980-12-11
734,1,6972,Ian McShane,1,Acting,1980-12-11

tv_shows_top_25_yearly.csv
year,name,id,genres,first_air_date,last_air_date,origin_country,rating,popularity
1980,"Magnum, P.I.",734,"10759, 80, 18, 9648",1980-12-11,1988-05-01,US,7.3,42.925
1980,Heathcliff,12803,16,1980-10-04,1981-12-05,US,6.2,27.677
1980,Shogun,13862,"10759, 18, 10768",1980-09-15,1980-09-19,US,7.7,21.489
1980,Richie Rich,3026,16,1980-11-08,1983-09-24,US,6.4,14.064
1980,Texas,3150,10766,1980-08-04,1982-12-31,US,5.7,13.302

join data to retrieve
tv_shows_top_25_yearly.csv
show_id, show_name, first_air_date, last_air_date

tv_show_season_to_cast.csv
season_number, cast_id, cast_name, episode_count, known_for_department,season_air_date

tv_show_cast_details.csv
gender as detail_gender

tv_cast_image_race_gender.csv
profile_path,profile_race,profile_gender