from twin_earth.models import Layer

def build_copernicus_land_service_url(layer: Layer, params):

    base_url = layer.service_url
    coordinates = params["bbox"].split(",") # " 'min_lat,min_lng,max_lat,max_lng' "
    lat = coordinates[0]
    lng = coordinates[1]

    if layer.type == Layer.LayerType.ARCGIS_MapServer:
        url = base_url + "/identify?"
        url += 'geometry={"x": ' + lat + ',"y":' + lng + '}'
        url += "&tolerance=1"
        url += "&mapExtent=" + str(lat-1) + "," + str(lng-1) + "," + str(lat+1) + "," + str(lng+1)
        url += "&imageDisplay=" + str(600) + "," + str(550) + ",96"
        url += "&geometryType=esriGeometryPoint&returnGeometry=false&returnCatalogItems=false&returnPixelValues=true&processAsMultidimensional=false&maxItemCount=1&f=pjson"

    elif layer.type == Layer.LayerType.ARCGIS_ImageServer:
        url = base_url + "/identify?"
        url += 'geometry={"x": ' + lat + ',"y":' + lng + '}'
        url += "&geometryType=esriGeometryPoint&returnGeometry=false&returnCatalogItems=false&returnPixelValues=true&processAsMultidimensional=false&maxItemCount=1&f=pjson"

    else:
        url = base_url + "?"
        url += "SERVICE=WMS&"
        url += "VERSION=1.3.0&"
        url += "REQUEST=GetFeatureInfo&"
        url += "FORMAT=image/png&"
        url += "TRANSPARENT=true&"
        url += "QUERY_LAYERS=" + layer.layer_name + "&"
        url += "TILED=true&"
        url += "LAYERS=" + layer.layer_name + "&"
        url += "BBOX=" + params["bbox"] + "&"
        url += "CRS=EPSG:3857&"

        #add the dimensions if present
        # dimensions are comma-separated
        for p in layer.parameters.split(","):
            if params.get(p):
                url += str(p) + "=" + str(params[p]) + "&"     
                
        url += "INFO_FORMAT=text/xml&"
        url += "I=0&J=0&WIDTH=1&HEIGHT=1&STYLES="
    
    return url

def coastal_zones_codes():
    return {
        11110: "Continuous urban fabric (IMD >=80%)",
        11120: "Dense urban fabric (IMD >= 30-80%)",
        11130: "Low urban fabric (IMD < 30%)",
        11210: "Industrial, commercial, public and military units (other)",
        11220: "Nuclear energy plants and associated land",
        12100: "Road networks and associated land",
        12200: "Railways and associated land",
        12310: "Cargo port",
        12320: "Passenger port",
        12340: "Naval port",
        12350: "Marinas",
        12360: "Local multi-functional harbours",
        12370: "Shipyards",
        12400: "Airports and associated land",
        13110: "Mineral extraction sites",
        13120: "Dump sites",
        13130: "Construction sites",
        13200: "Land without current use",
        14000: "Green urban, sports and leisure facilities",
        21100: "Arable irrigated and non-irrigated land",
        21200: "Greenhouses",
        22100: "Vineyards, fruit trees and berry plantations",
        22200: "Olive groves",
        23100: "Annual crops associated with permanent crops",
        23200: "Complex cultivation patterns",
        23300: "Land principally occupied by agriculture with significant areas of natural vegetation",
        23400: "Agro-forestry",
        31100: "Natural & semi-natural broadleaved forest",
        31200: "Highly artificial broadleaved plantations",
        32100: "Natural & semi-natural coniferous forest",
        32200: "Highly artificial coniferous plantations",
        33100: "Natural & semi-natural mixed forest",
        33200: "Highly artificial mixed plantations",
        34000: "Transitional woodland and scrub",
        35000: "Lines of trees and scrub",
        36000: "Damaged forest",
        41000: "Managed grassland",
        42100: "Semi-natural grassland",
        42200 : "Alpine and sub-alpine natural grassland",
        51000: "Heathland and moorland",
        52000: "Alpine scrub land",
        53000: "Sclerophyllous scrubs",
        61100: "Sparse vegetation on sands",
        61200: "Sparse vegetation on rocks",
        62111: "Sandy beaches",
        62112: "Shingle beaches",
        62120: "Dunes",
        62200: "River banks",
        63110: "Bare rocks and outcrops",
        63120: "Coastal cliffs",
        63200: "Burnt areas (except burnt forest)",
        63300: "Glaciers and perpetual snow",
        71100: "Inland marshes",
        71210: "Exploited peat bogs",
        71220: "Unexploited peat bogs",
        72100: "Salt marshes",
        72200: "Salines",
        72300: "Intertidal flats",
        81100: "Natural & semi-natural water courses",
        81200: "Highly modified water courses and canals",
        81300: "Seasonally connected water courses (oxbows)",
        82100: "Natural lakes",
        82200: "Reservoirs",
        82300: "Aquaculture ponds",
        82400: "Standing water bodies of extractive industrial sites",
        83100: "Lagoons",
        83200: "Estuaries",
        83300: "Marine inlets and fjords",
        84100: "Open sea",
        84200: "Coastal waters"
    }

def corine_land_cover_codes():
    return {
        111: "Continuous urban fabric",
        112: "Discontinuous urban fabric",
        121: "Industrial and commercial units",
        122: "Road and rail networks and associated land",
        123: "Port areas",
        124: "Airports",
        131: "Mineral extraction sites",
        132: "Dump sites",
        133: "Construction sites",
        141: "Green urban areas",
        142: "Sport and leisure facilities",

        211: "Non-irrigated arable land",
        212: "Permanently irrigated land",
        213: "Rice fields",
        221: "Vineyards",
        222: "Fruit trees and berry plantations",
        223: "Olive groves",
        231: "Pastures",
        241: "Annual crops associated with permanent crops",
        242: "Complex cultivation patterns",
        243: "Land principally occupied by agriculture, with significant areas of natural vegetation",
        244: "Agro-forestry areas",
        311: "Broad-leaved forest",
        312: "Coniferous forest",
        313: "Mixed forest",
        321: "Natural grassland",
        322: "Moors and heathland",
        323: "Sclerophyllous vegetation",
        324: "Transitional woodland-shrub",
        331: "Beaches, dunes, sands",
        332: "Bare rocks",
        333: "Sparsely vegetated areas",
        334: "Burnt areas",
        335: "Glaciers and perpetual snow",
        411: "Inland marshes",
        412: "Peat bogs",
        421: "Salt marshes",
        422: "Salines",
        423: "Intertidal flats",
        511: "Water courses",
        512: "Water bodies",
        521: "Coastal lagoons",
        522: "Estuaries",
        523: "Sea and ocean"
    }

def waw_codes():
    return {
        0: "Dry",
        1: "Permanent water",
        2: "Temporary water",
        3: "Permanent wet",
        4: "Temporary wet",
        253: "Sea water",
        254: "Unclassifiable",
        255: "Outside area"
    }

def forest_type_codes():
    return {
        0: "All non-forest areas",
        1: "Broadleaved forest",
        2: "Coniferous forest",
        255: "Outside area"
    }

def built_up_categories():
    return {
        0: "Non built-up",
        1: "Built-up",
        255: "Outside area"
    }
    