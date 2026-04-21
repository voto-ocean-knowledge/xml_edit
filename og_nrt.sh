glider=$1
mission=$2
missiondir=/Data/OG_nrt/$glider/M$mission/timeseries
xmlname=/home/usrerddap/erddap/xml_edit/xml/OG_nrt_"$glider"_M$mission"".xml
docker exec -i docker-erddap bash -c "cd webapps/erddap/WEB-INF/ && bash GenerateDatasetsXml.sh EDDTableFromMultidimNcFiles $missiondir .\* nothing default default default default default default default default default default default default default default default default"
cp /data/erddapData/logs/GenerateDatasetsXml.out "$xmlname"
/usr/bin/python3 /home/usrerddap/erddap/xml_edit/correct_xml.py  "$glider" "$mission" OG_nrt

flagdir=/data/erddapData/hardFlag/OG_nrt_"$glider"_M"$mission"
touch "$flagdir"