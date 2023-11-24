cd /home/ubuntu/erddapContent
cat header.xml > new_datasets.xml
for f in parts/nrt_*SEA*.xml; do tail -q -n +2 "$f" >> new_datasets.xml && echo "" >> new_datasets.xml; done
for f in parts/delayed_*SEA*.xml; do tail -q -n +2 "$f" >> new_datasets.xml && echo "" >> new_datasets.xml; done
for f in parts/adcp_*SEA*.xml; do tail -q -n +2 "$f" >> new_datasets.xml && echo "" >> new_datasets.xml; done
tail -q -n +2  parts/ctd_deployment.xml >> new_datasets.xml && echo "" >> new_datasets.xml
for f in parts/meta_*.xml; do tail -q -n +2 "$f" >> new_datasets.xml && echo "" >> new_datasets.xml; done
echo "</erddapDatasets>"  >> new_datasets.xml
mv new_datasets.xml datasets.xml
