glider=$1
mission=$2
missiondir=/Data/OG_complete/$glider/M$mission/timeseries
xmlname=/home/usrerddap/erddap/xml_edit/xml/OG_complete_"$glider"_M$mission"".xml
docker exec -i docker-erddap bash -c "cd webapps/erddap/WEB-INF/ && java -cp classes:../../../lib/servlet-api.jar:lib/* -Xms6000M -Xmx6000M gov.noaa.pfel.erddap.GenerateDatasetsXml EDDTableFromMultidimNcFiles $missiondir .\* nothing default default default default default default default default default default default default default default default default"
cp /data/erddapData/logs/GenerateDatasetsXml.out "$xmlname"
/usr/bin/python3 /home/usrerddap/erddap/xml_edit/og1_xml.py  "$glider" "$mission"

flagdir=/data/erddapData/hardFlag/OG_complete_"$glider"_M"$mission"
touch "$flagdir"