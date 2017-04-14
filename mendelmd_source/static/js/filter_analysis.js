function formSubmit() {
    newwindow = document.getElementById("newwindow");
    if(newwindow.checked == true)
        document.getElementById("filterform").target = "_blank";
    document.getElementById("filterform").submit();
    //document.getElementById('loading_img').style.display = "block";
    $('#loading_img').show();
    $('#loading_img2').show();
}

function recessive(){
oFormObject = document.forms['filterform'];
oFormObject.elements["mutation_type"][1].selected = true;
}
function dominant(){
oFormObject = document.forms['filterform'];
oFormObject.elements["mutation_type"][2].selected = true;
}
function x_linked_recessive(){
oFormObject = document.forms['filterform'];
oFormObject.elements["chr"].value = 'X';
oFormObject.elements["mutation_type"][1].selected = true;
}
function x_linked_dominant(){
oFormObject = document.forms['filterform'];
oFormObject.elements["chr"].value = 'X';
oFormObject.elements["mutation_type"][2].selected = true;
}
function compound_heterozygous(){
oFormObject = document.forms['filterform'];
oFormObject.elements["mutation_type"][2].selected = true;
oFormObject.elements["variants_per_gene_option"][1].selected = true;
oFormObject.elements["variants_per_gene"].value = '2';
}
