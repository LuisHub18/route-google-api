from dotenv import load_dotenv
import googlemaps
import os
import csv
load_dotenv()

gmaps = googlemaps.Client(key=os.getenv('API_KEY'))

points = {
    "forum" : (24.814255766993092, -107.40069025553083),
    "explanada" : (24.746813970159995, -107.44599053226524),
    "tec_culiacan" : (24.789105722097062, -107.39670416109986),
    "ceiba" : (24.79848761268018, -107.4231976034287),
    "catedral" : (24.808844787599703, -107.39406046109939),
    "estadio_tomateros" : (24.798925888956187, -107.38997589414312),
    "parque_riberas" : (24.8130087000168, -107.3891793072115),
    "parque_87" : (24.773593786354102, -107.38861731743529),
    "parque_acuatico": (24.80812955949714, -107.40794481027028),
    "plaza_sendero": (24.825444175827357, -107.42706774393118),
    "zoo_culiacan": (24.814883270179752, -107.38424246468543),
    "aeropuerto": (24.767827561065104, -107.47018750115168),
    "splash_club": (24.73110314693567, -107.34740119877841),
    "plaza_san_isidro": (24.755952183680453, -107.40270133061294),
    "jardin_botanico": (24.827146880138784, -107.3859378744943),
    "plaza_pabellon":(24.80403532723677, -107.34387579458584),
    "lomita": (24.789922976167656, -107.393827599695),
    "hospital_general": (24.794560572980007, -107.38695941812759),
    "imss": (24.79741997857549, -107.39011115045139),
    "plaza_ventura": (24.813700381413142, -107.40864841582747),
}

# Calcula las distancias entre todos los pares de puntos
distances = {}
for origin_name, origin_coords in points.items():
    for destination_name, destination_coords in points.items():
        if origin_name != destination_name:
            distance = gmaps.distance_matrix(origin_coords, destination_coords)['rows'][0]['elements'][0]['distance']['value']
            distances[(origin_name, destination_name)] = distance

# Guarda las distancias en un archivo CSV
with open('distances.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Origen', 'Destino', 'Distancia'])
    for (origin, destination), distance in distances.items():
        writer.writerow([origin, destination, distance])


