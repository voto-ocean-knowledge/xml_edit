glider=$1
mission=$2

sudo docker exec -it erddap-docker_erddap_1 bash -c "cd webapps/erddap/WEB-INF/ && bash GenerateDatasetsXml.sh EDDTableFromMultidimNcFiles /Data/nrt/SEA$glider/M$mission/timeseries .\* nothing 'time, latitude, longitude, depth' default default default default default default default default default default default default default default  "
cp /media/data/customdocker/customvolumes/erddapData/logs/GenerateDatasetsXml.out /home/ubuntu/xml_edit/original.xml
/usr/bin/python3 /home/ubuntu/xml_edit/correct_xml.py  "$glider" "$mission" nrt