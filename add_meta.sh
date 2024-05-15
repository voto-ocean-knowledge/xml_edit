name=$1
missiondir=/Data/meta
xmlname=/home/usrerddap/erddap/xml_edit/xml/$name.xml
docker exec -i docker-erddap bash -c "cd webapps/erddap/WEB-INF/ && bash GenerateDatasetsXml.sh EDDTableFromAsciiFiles $missiondir $name.csv nothing default default default \; default default default default default default default default default default default default default"
cp /data/erddapData/logs/GenerateDatasetsXml.out "$xmlname"
/usr/bin/python3 /home/usrerddap/erddap/xml_edit/correct_meta.py "$name"
metaname=meta_$name
bash /home/usrerddap/erddap/xml_edit/make_datasets.sh
flagdir=/data/erddapData/hardFlag/$metaname
touch "$flagdir"
