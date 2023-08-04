missiondir=/Data/ctd
xmlname=/home/ubuntu/erddapContent/parts/ctd_deployment.xml
docker exec -i docker-erddap bash -c "cd webapps/erddap/WEB-INF/ && bash GenerateDatasetsXml.sh EDDTableFromMultidimNcFiles $missiondir ctd_deployment.nc nothing 'time' default default default default default default default default default default default default default default default"
cp /media/data/erddapData/logs/GenerateDatasetsXml.out "$xmlname"
bash /home/ubuntu/xml_edit/make_datasets.sh
flagdir=/media/data/erddapData/hardFlag/ctd_deployment
touch "$flagdir"
