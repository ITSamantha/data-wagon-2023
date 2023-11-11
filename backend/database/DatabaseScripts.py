selectAllStationsQuery = 'SELECT st_id, latitude, longitude FROM public."Stations";'
selectAllRoadsQuery = str('SELECT start_id, end_id, len, id FROM public."Roads";')
selectRoadsByStartStationQuery = '''
    SELECT start_id, end_id, len, id FROM public."Roads" 
    WHERE start_id = %s;
'''
selectStationsByRadiusQuery = (
        'SELECT st_id, latitude, longitude FROM public."Stations" '
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