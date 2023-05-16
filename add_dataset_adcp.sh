glider=$1
mission=$2
missiondir=/Data/complete_mission/SEA$glider/M$mission/ADCP
xmlname=/home/ubuntu/xml_edit/xml/adcp_SEA"$glider"_M$mission"".xml
sudo docker exec -i docker-erddap bash -c "cd webapps/erddap/WEB-INF/ && java -cp classes:../../../lib/servlet-api.jar:lib/* -Xms6000M -Xmx6000M gov.noaa.pfel.erddap.GenerateDatasetsXml EDDGridFromNcFiles  $missiondir .\* nothing default default default default default default default default default default default default default default default default "
cp /media/data/erddapData/logs/GenerateDatasetsXml.out "$xmlname"
/usr/bin/python3 /home/ubuntu/xml_edit/correct_xml.py "$glider" "$mission" adcp

flagdir=/media/data/erddapData/hardFlag/adcp_SEA0"$glider"_M"$mission"
touch "$flagdir"
