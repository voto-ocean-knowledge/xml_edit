for f in /data/meta/*;
do
        name=$(basename "${f%.*}")
        /usr/bin/bash /home/usrerddap/erddap/xml_edit/add_meta.sh "$name"
done
