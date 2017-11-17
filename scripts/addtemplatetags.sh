echo '{% load static i18n %}
' > ../templates/dashboard.html
cat ../static/adminlte/index.html >> ../templates/dashboard.html
sed -i -e 's/href="bower_components/href="{% static "adminlte\/bower_components/g' ../templates/dashboard.html
sed -i -e 's/href="dist/href="{% static "adminlte\/dist/g' ../templates/dashboard.html
sed -i -e 's/.css">/.css" %}">/g' ../templates/dashboard.html
sed -i -e 's/src="dist/src="{% static "adminlte\/dist/g' ../templates/dashboard.html
sed -i -e 's/.jpg"/.jpg" %}"/g' ../templates/dashboard.html
sed -i -e 's/src="bower_components/src="{% static "adminlte\/bower_components/g' ../templates/dashboard.html
sed -i -e 's/.js"/.js" %}"/g' ../templates/dashboard.html
sed -i -e 's/src="plugins/src="{% static "adminlte\/plugins/g' ../templates/dashboard.html