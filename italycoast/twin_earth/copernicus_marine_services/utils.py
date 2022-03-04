import datetime
import requests
import xml.etree.ElementTree as ET
import twin_earth.models as dte_models

def update_layers(wms_list):
    # wms list is a list of wms urls
    for url in wms_list:
        try:
            urlSuffix = "?request=GetCapabilities&service=WMS&VERSION=1.3.0"
            complete_url = url + urlSuffix
            namespaces = {
                "opengis": "http://www.opengis.net/wms" 
            }

            category = None
            if "med-cmcc" in url:
                category = dte_models.Category.objects.all().get(name="Sea Physics")
            elif "med-hcmr" in url:
                category = dte_models.Category.objects.all().get(name="Sea Waves")
            elif "med-ogs" in url or "cmems_obs_oc_med_bgc_tur" in url:
                category = dte_models.Category.objects.all().get(name="Sea Biogeochemistry")
            elif "cmems_obs-sl_med_phy" in url:
                category = dte_models.Category.objects.all().get(name="Sea Dynamic Topography")
            elif "dataset-duacs" in url:
                category = dte_models.Category.objects.all().get(name="Sea Level")
            elif "dataset-oc-med-chl" in url:
                category = dte_models.Category.objects.all().get(name="Ocean Chlorophyll")
            elif "SST_MED_SST" in url or "METEOFRANCE-EUR-SST-L4-NRT-OBS_FULL_TIME_SERIE" in url:
                category = dte_models.Category.objects.all().get(name="Sea Temperature")

            xml_GetCapabilities = requests.get(complete_url)
            xml_text = xml_GetCapabilities.text
            xml = ET.fromstring(xml_text)

            #["WMS_Capabilities"]["Capability"][0]["Layer"][0]["Layer"][0]["Layer"][0]["Dimension"]
            layers_parent = xml.find(f"opengis:Capability/opengis:Layer/opengis:Layer", namespaces=namespaces)
            title = layers_parent.find(f"opengis:Title", namespaces=namespaces).text
            frequency = ""
            if "Daily" in title:
                frequency = "daily"
            elif "Monthly" in title:
                frequency = "monthly"
            elif "15 Minutes" in title:
                frequency = "15-minutes"
            else:
                frequency = "hourly"

            if "-" in title:
                layer_name_suffix = title.split("-")[1].strip()
            else:
                layer_name_suffix = ""

            layers_list = layers_parent.findall(f"opengis:Layer", namespaces=namespaces)
            for layer in layers_list:
                layer_name = layer.find(f"opengis:Name", namespaces=namespaces).text
                layer_title = layer.find(f"opengis:Title", namespaces=namespaces).text.replace("_"," ").title()
                layer_abstract = layer.find(f"opengis:Abstract", namespaces=namespaces).text
                readable_name = layer_title + " " + layer_name_suffix
                dimensions = layer.findall(f"opengis:Dimension", namespaces=namespaces)
                parameters = ""
                start_time = None
                end_time = None
                for dim in dimensions:
                    param_name = dim.attrib["name"]
                    parameters += param_name + ","
                    if param_name == "time":
                        try:
                            #time format 2019-05-01T00:00:00.000Z/2021-11-12T23:45:00.000Z/PT15M,...
                            time_list = dim.text.strip().split(",")
                            first = time_list[0].strip()
                            last = time_list[len(time_list)-1].strip()

                            if "/" in first:
                                first = first.split("/")[0]
                            if "/" in last:
                                last = last.split("/")[1]
                            
                            first = first.split("T")
                            last = last.split("T")

                            start_time = first[0]
                            end_time = last[0]
                        except Exception as ex:
                            print(ex)
                
                if len(parameters) > 0: 
                    parameters = parameters[0: len(parameters)-1]


                db_layer = dte_models.Layer.objects.all().filter(layer_name=layer_name, readable_name=readable_name, description=layer_abstract, frequency=frequency)
                if not db_layer.exists():
                    db_layer = dte_models.Layer(
                        source = "Copernicus Marine Services",
                        layer_name = layer_name,
                        readable_name = readable_name,
                        description = layer_abstract,
                        keywords = "",
                        type = "WMS",
                        parameters = parameters,
                        category = category,
                        frequency = frequency,

                        service_url = url,
                        metadata_url = url,
                        legend_url = url, 
                        more_data_url = url,
                        copyright = url,

                        initial_time_range = start_time,
                        final_time_range = end_time
                    )
                else:
                    db_layer = db_layer.first()
                    db_layer.source = "Copernicus Marine Services"
                    db_layer.layer_name = layer_name
                    db_layer.readable_name = readable_name
                    db_layer.description = layer_abstract
                    db_layer.keywords = ""
                    db_layer.type = "WMS"
                    db_layer.parameters = parameters
                    db_layer.category = category
                    db_layer.frequency = frequency

                    db_layer.service_url = url
                    db_layer.metadata_url = url
                    db_layer.legend_url = url
                    db_layer.more_data_url = url
                    db_layer.copyright = url

                    db_layer.initial_time_range = start_time
                    db_layer.final_time_range = end_time

                db_layer.save()
            xml = None
        except Exception as ex:
            print(ex)
            

def format_time_intervals(time_list):
    complete_list = []
    for element in time_list:
        split_interval = element.strip().split("/")
        if len(split_interval) > 1:
            interval_list = []
            #Extract dates with timezone as it comes from the service -- Format: 2021-10-28T23:30:00.000Z
            first_date = datetime.datetime.strptime(split_interval[0], "%Y-%m-%dT%H:%M:%S.000Z")
            end_date = datetime.datetime.strptime(split_interval[1], "%Y-%m-%dT%H:%M:%S.000Z")
            
            interval = split_interval[2]

            if "PT1H" in interval: #Hourly
                # 2021-03-29T00:30:00.000Z/2021-10-28T23:30:00.000Z/PT1H For Hourly
                while first_date <= end_date: 
                    month = f'0{first_date.month}' if len(str(first_date.month)) == 1 else f'{first_date.month}'
                    day = f'0{first_date.day}' if len(str(first_date.day)) == 1 else f'{first_date.day}'
                    hours = f'0{first_date.hour}' if len(str(first_date.hour)) == 1 else f'{first_date.hour}'
                    minutes = f'0{first_date.minute}' if len(str(first_date.minute)) == 1 else f'{first_date.minute}'
                    date_to_add = f'{first_date.year}-{month}-{day}T{hours}:{minutes}:00.000Z'
                    interval_list.append(date_to_add)
                    first_date = first_date + datetime.timedelta(hours=1)
            
            elif "P30DT12H" in interval: #Monthly
                # 2019-05-16T12:00:00.000Z/2019-07-16T12:00:00.000Z/P30DT12H For monthly
                while first_date <= end_date: 
                    month = f'0{first_date.month}' if len(str(first_date.month)) == 1 else f'{first_date.month}'
                    day = f'0{first_date.day}' if len(str(first_date.day)) == 1 else f'{first_date.day}'
                    hours = f'0{first_date.hour}' if len(str(first_date.hour)) == 1 else f'{first_date.hour}'
                    minutes = f'0{first_date.minute}' if len(str(first_date.minute)) == 1 else f'{first_date.minute}'
                    date_to_add = f'{first_date.year}-{month}-{day}T{hours}:{minutes}:00.000Z'
                    interval_list.append(date_to_add)
                    first_date = first_date + datetime.timedelta(hours=24*30 + 12) #30 days + 12 hours

            elif "P31D" in interval: #31 days
                while first_date <= end_date: 
                    month = f'0{first_date.month}' if len(str(first_date.month)) == 1 else f'{first_date.month}'
                    day = f'0{first_date.day}' if len(str(first_date.day)) == 1 else f'{first_date.day}'
                    hours = f'0{first_date.hour}' if len(str(first_date.hour)) == 1 else f'{first_date.hour}'
                    minutes = f'0{first_date.minute}' if len(str(first_date.minute)) == 1 else f'{first_date.minute}'
                    date_to_add = f'{first_date.year}-{month}-{day}T{hours}:{minutes}:00.000Z'
                    interval_list.append(date_to_add)
                    first_date = first_date + datetime.timedelta(hours=24*31) #31 days

            elif "P1D" in interval: #Daily
                # 2019-05-01T12:00:00.000Z/2021-11-02T12:00:00.000Z/P1D For Daily
                while first_date <= end_date: 
                    month = f'0{first_date.month}' if len(str(first_date.month)) == 1 else f'{first_date.month}'
                    day = f'0{first_date.day}' if len(str(first_date.day)) == 1 else f'{first_date.day}'
                    hours = f'0{first_date.hour}' if len(str(first_date.hour)) == 1 else f'{first_date.hour}'
                    minutes = f'0{first_date.minute}' if len(str(first_date.minute)) == 1 else f'{first_date.minute}'
                    date_to_add = f'{first_date.year}-{month}-{day}T{hours}:{minutes}:00.000Z'
                    interval_list.append(date_to_add)
                    first_date = first_date + datetime.timedelta(hours=24)

            elif "PT15M" in interval: #15-minutes
                # 2019-05-01T00:00:00.000Z/2021-10-28T23:45:00.000Z/PT15M For 15 minutes
                while first_date <= end_date: 
                    month = f'0{first_date.month}' if len(str(first_date.month)) == 1 else f'{first_date.month}'
                    day = f'0{first_date.day}' if len(str(first_date.day)) == 1 else f'{first_date.day}'
                    hours = f'0{first_date.hour}' if len(str(first_date.hour)) == 1 else f'{first_date.hour}'
                    minutes = f'0{first_date.minute}' if len(str(first_date.minute)) == 1 else f'{first_date.minute}'
                    date_to_add = f'{first_date.year}-{month}-{day}T{hours}:{minutes}:00.000Z'
                    interval_list.append(date_to_add)
                    first_date = first_date + datetime.timedelta(minutes=15)

            complete_list += interval_list 
        else: 
            complete_list.append(element)  

    return complete_list