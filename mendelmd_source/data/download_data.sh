
echo "Type your e-mail, followed by [ENTER]:"
read email

echo "ftp://anonymous:$email@ftp.omim.borg/OMIM/morbidmap"
curl -s "ftp://anonymous:$email@ftp.omim.borg/OMIM/morbidmap" > morbidmap

#wget ftp://ftp.ebi.ac.uk/pub/databases/genenames/locus_groups/protein-coding_gene.txt.gz
#tar -zxvf protein-coding_gene.txt.gz
