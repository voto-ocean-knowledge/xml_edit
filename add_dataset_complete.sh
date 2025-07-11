glider=$1
mission=$2
missiondir=/Data/complete_mission/$glider/M$mission/timeseries
xmlname=/home/usrerddap/erddap/xml_edit/xml/delayed_"$glider"_M$mission"".xml
docker exec -i docker-erddap bash -c "cd webapps/erddap/WEB-INF/ && java -cp classes:../../../lib/servlet-api.jar:lib/* -Xms6000M -Xmx6000M gov.noaa.pfel.erddap.GenerateDatasetsXml   EDDTableFromMultidimNcFiles $missiondir .\* nothing 'time' default default default default default default default default default default default default default default default"
cp /data/erddapData/logs/GenerateDatasetsXml.out "$xmlname"
/usr/bin/python3 /home/usrerddap/erddap/xml_edit/correct_xml.py  "$glider" "$mission" delayed

flagdir=/data/erddapData/hardFlag/delayed_"$glider"_M"$mission"
touch "$flagdir"
