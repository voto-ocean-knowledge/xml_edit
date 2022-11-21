glider=$1
mission=$2
missiondir=/Data/complete_mission/SEA$glider/M$mission/timeseries_chunked
xmlname=/home/ubuntu/xml_edit/xml/delayed_SEA"$glider"_M$mission"".xml
sudo docker exec -i erddap-docker_erddap_1 bash -c "cd webapps/erddap/WEB-INF/ && java -cp classes:../../../lib/servlet-api.jar:lib/* -Xms8000M -Xmx8000M gov.noaa.pfel.erddap.GenerateDatasetsXml EDDTableFromMultidimNcFiles $missiondir .\* nothing 'time' default default default default default default default default default default default default default default  "
cp /media/data/customdocker/customvolumes/erddapData/logs/GenerateDatasetsXml.out "$xmlname"
/usr/bin/python3 /home/ubuntu/xml_edit/correct_xml.py  "$glider" "$mission" delayed

flagdir=/media/data/customdocker/customvolumes/erddapData/flag/delayed_SEA0"$glider"_M"$mission"
touch "$flagdir"
