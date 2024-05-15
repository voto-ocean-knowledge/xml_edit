missiondir=/Data/ctd
xmlname=/home/usrerddap/erddap/xml_edit/xml/ctd_deployment.xml
docker exec -i docker-erddap bash -c "cd webapps/erddap/WEB-INF/ && bash GenerateDatasetsXml.sh EDDTableFromMultidimNcFiles $missiondir ctd_deployment.nc nothing 'time' default default default default default default default default default default default default default default default"
cp /data/erddapData/logs/GenerateDatasetsXml.out "$xmlname"
bash /home/usrerddap/erddap/xml_edit/make_datasets.sh
/usr/bin/python3 /home/usrerddap/erddap/xml_edit/correct_ctd.py ctd_deployment
flagdir=/data/erddapData/hardFlag/ctd_deployment
touch "$flagdir"
