cd /home/usrerddap/erddap/content
cat header.xml > new_datasets.xml
for f in parts/nrt_*.xml; do tail -q -n +2 "$f" >> new_datasets.xml && echo "" >> new_datasets.xml; done
for f in parts/delayed_*.xml; do tail -q -n +2 "$f" >> new_datasets.xml && echo "" >> new_datasets.xml; done
for f in parts/meta_*.xml; do tail -q -n +2 "$f" >> new_datasets.xml && echo "" >> new_datasets.xml; done
tail -q -n +2  parts/ctd_deployment.xml >> new_datasets.xml && echo "" >> new_datasets.xml
tail -q -n +2  parts/ad2cp.xml >> new_datasets.xml && echo "" >> new_datasets.xml
cat  parts/requests.xml >> new_datasets.xml && echo "" >> new_datasets.xml
cat  parts/locations.xml >> new_datasets.xml && echo "" >> new_datasets.xml
cat  parts/SB2120_M3_delayed.xml >> new_datasets.xml && echo "" >> new_datasets.xml
echo "</erddapDatasets>"  >> new_datasets.xml
mv new_datasets.xml datasets.xml
