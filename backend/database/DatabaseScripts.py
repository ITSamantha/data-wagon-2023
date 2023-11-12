selectAllStationsQuery = 'SELECT st_id, latitude, longitude FROM public."Stations";'
selectAllRoadsQuery = str('SELECT start_id, end_id, len, id FROM public."Roads";')
selectRoadsByStartStationQuery = '''
    SELECT start_id, end_id, len, id FROM public."Roads" 
    WHERE start_id = %s;
'''
selectStationsByRadiusQuery = (
        'SELECT st_id, latitude, longitude, end_id, len, public."Roads".id FROM public."Stations" '
        + 'INNER JOIN public."Roads" ON start_id = st_id '
        + 'WHERE ( '
        + '(ABS(longitude - %s) <= %s )'
        + ' AND '
        + '(ABS(latitude - %s) <= %s)'
        + ')'
)

insertRoadQuery = (
        'INSERT INTO public."Roads"('
        + 'start_id, end_id, len'
        + ') '
        + 'VALUES ( '
        + '%s, %s, %s'
        + ');'
)

insertStationsQuery = (
        'INSERT INTO public."Stations"('
        + 'st_id, latitude, longitude'
        + ') '
        + 'VALUES ( '
        + '%s, %s, %s'
        + ');'
)

deleteStationsQuery = '''
    DELETE FROM public."Stations"
'''

deleteRoadsQuery = '''
    DELETE FROM public."Roads"
'''

selectStationByIdQuery = '''
    SELECT st_id, latitude, longitude
	FROM public."Stations"
	WHERE st_id = %s
	;
'''

insertDestQuery = '''
INSERT INTO public."Destinations"(
	wag_id, oper_date, disl_st_id, dest_st_id, train_id, form_st_id, target_st_id)
	VALUES ( 
	%s, %s, %s, %s, %s, %s, %s);
	'''

selectDestinationsByTrain = '''

select  oper_date, 
disl_st_id

 from public."Destinations" 
where train_id = %s and oper_date >= (
SELECT  oper_date FROM public."Destinations"
where train_id = %s AND disl_st_id = form_st_id 
order by oper_date DESC LIMIT 1)
GROUP BY oper_date,  disl_st_id
order by oper_date ASC 
;


'''

selectDestinationsActual = '''
select 
distinct on (train_id) 
max(oper_date) as d, train_id,  disl_st_id as d_id, st.latitude, st.longitude  
from public."Destinations"
inner join public."Stations" as st on disl_st_id = st_id
where oper_date >= (
select oper_date - interval '12 hours' from public."Destinations"
order by oper_date DESC LIMIT 1
	)
group by  train_id, d_id, st.latitude, st.longitude  
order by train_id, d DESC
'''
