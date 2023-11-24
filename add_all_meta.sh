for f in /media/data/meta/*;
do
        name=$(basename "${f%.*}")
        /usr/bin/bash /home/ubuntu/xml_edit/add_meta.sh "$name"
done
