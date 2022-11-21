glider=$1
mission=$2
missiondir=/Data/nrt/SEA$glider/M$mission/timeseries
xmlname=/home/ubuntu/xml_edit/xml/nrt_SEA"$glider"_M$mission"".xml
sudo docker exec -i erddap-docker_erddap_1 bash -c "cd webapps/erddap/WEB-INF/ && bash GenerateDatasetsXml.sh EDDTableFromMultidimNcFiles $missiondir .\* nothing 'time' default default default default default default default default default default default default default default  "
cp /media/data/customdocker/customvolumes/erddapData/logs/GenerateDatasetsXml.out "$xmlname"
/usr/bin/python3 /home/ubuntu/xml_edit/correct_xml.py  "$glider" "$mission" nrt

flagdir=/media/data/customdocker/customvolumes/erddapData/flag/nrt_SEA0"$glider"_M"$mission"
touch "$flagdir"