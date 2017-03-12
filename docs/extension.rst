Extension
=========

Here we describe the steps to extend Mendel,MD and add a new options for annotation and filtering.

1)	Create the necessary field to store this data on variants/models.py app.
2)	Create the form to filter this data (Ex. slide, select box or input text field) on filter_analysis/forms.py
3)	Create the method that will filter this field on filter_analysis/filter_variants.py.
4)	Add the field as a column in the filter_analysis/templates of the variants template form.
