

$(function () {


oFormObject = document.forms['filterform'];

oFormObject.elements["genes_in_common"].checked = true;
// oFormObject.elements["exclude_varisnp"].checked = true;

// oFormObject.elements["exclude_segdup"].checked = true;
oFormObject.elements["read_depth_option"][1].selected = true;
oFormObject.elements["read_depth"].value = '10';

oFormObject.elements["impact"][1].selected = true;
oFormObject.elements["impact"][0].selected = true;
oFormObject.elements["dbsnp_option"].value = '>';
oFormObject.elements["dbsnp_build"].value = '130';
oFormObject.elements["genomes1000"].value = '0 - 0.01';
oFormObject.elements["dbsnp_frequency"].value = '0 - 0.01';
oFormObject.elements["esp_frequency"].value = '0 - 0.01';

});