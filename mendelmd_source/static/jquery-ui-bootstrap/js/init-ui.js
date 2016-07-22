$(function () {

    

    //SIFT
    $( "#sift-slider-range" ).slider({
            range: true,
            min: 0,
            max: 1,
	    	step: 0.01,
            values: [ 0, 1 ],
            slide: function( event, ui ) {  $( "#id_sift" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    sift_value = $("#id_sift").val();
    if (sift_value) {
    	value_range =sift_value.split(" - ");
    	$("#sift-slider-range").slider('values',[value_range[0], value_range[1]]);
    }
    //Polyphen 2
    $( "#pp2-slider-range" ).slider({
            range: true,
            min: 0,
            max: 1,
	    	step: 0.01,
            values: [ 0, 1 ],
            slide: function( event, ui ) {  $( "#id_polyphen" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    pp2_value = $("#id_polyphen").val();
    if (pp2_value) {
    	value_range =pp2_value.split(" - ");
    	$("#pp2-slider-range").slider('values',[value_range[0], value_range[1]]);
    }
    //CADD
    $( "#cadd-slider-range" ).slider({
            range: true,
            min: 0,
            max: 20,
            step: 0.1,
            values: [ 0, 20 ],
            slide: function( event, ui ) {  $( "#id_cadd" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    cadd_value = $("#id_cadd").val();
    if (cadd_value) {
        value_range =cadd_value.split(" - ");
        $("#cadd-slider-range").slider('values',[value_range[0], value_range[1]]);
    }
    //rf score
    $( "#rf-slider-range" ).slider({
            range: true,
            min: 0,
            max: 1,
            step: 0.05,
            values: [ 0, 1 ],
            slide: function( event, ui ) {  $( "#id_rf_score" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    rf_value = $("#rf_score").val();
    if (rf_value) {
        value_range =rf_value.split(" - ");
        $("#rf-slider-range").slider('values',[value_range[0], value_range[1]]);
    }
    //ada score
    $( "#ada-slider-range" ).slider({
            range: true,
            min: 0,
            max: 1,
            step: 0.05,
            values: [ 0, 1 ],
            slide: function( event, ui ) {  $( "#id_ada_score" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    ada_value = $("#id_cadd").val();
    if (ada_value) {
        value_range =ada_value.split(" - ");
        $("#ada-slider-range").slider('values',[value_range[0], value_range[1]]);
    }
    //1000genomes
    $( "#g1000-slider-range" ).slider({
            range: true,
            min: 0,
            max: 0.5,
	    	step: 0.001,
            values: [ 0, 0.5 ],
            slide: function( event, ui ) {  $( "#id_genomes1000" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    g1000_value = $("#id_genomes1000").val();
    if (g1000_value) {
    	value_range =g1000_value.split(" - ");
    	$("#g1000-slider-range").slider('values',[value_range[0], value_range[1]]);
    }
    //dbsnp
    $( "#dbsnp-slider-range" ).slider({
            range: true,
            min: 0,
            max: 0.5,
	    	step: 0.001,
            values: [ 0, 0.5 ],
            slide: function( event, ui ) {  $( "#id_dbsnp_frequency" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    dbsnp_value = $("#id_dbsnp_frequency").val();
    if (dbsnp_value) {
    	value_range =dbsnp_value.split(" - ");
    	$("#dbsnp-slider-range").slider('values',[value_range[0], value_range[1]]);
    }
    //esp
    $( "#esp-slider-range" ).slider({
            range: true,
            min: 0,
            max: 0.5,
	    	step: 0.001,
            values: [ 0, 0.5 ],
            slide: function( event, ui ) {  $( "#id_esp_frequency" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    esp_value = $("#id_esp_frequency").val();
    if (esp_value) {
    	value_range =esp_value.split(" - ");
    	$("#esp-slider-range").slider('values',[value_range[0], value_range[1]]);
    }
    //hi_score
    $( "#hi-slider-range" ).slider({
            range: true,
            min: 0,
            max: 100,
            step: 0.1,
            values: [ 0, 100 ],
            slide: function( event, ui ) {  $( "#id_hi_frequency" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    hi_value = $("#id_hi_frequency").val();
    if (hi_value) {
        value_range =hi_value.split(" - ");
        $("#hi-slider-range").slider('values',[value_range[0], value_range[1]]);
    }

    //1000genomes
	$("#id_genomes1000_exclude").click(function(){
		if ($("#id_genomes1000_exclude").is(":checked"))
		{$("#g1000-slider-range").slider('disable');}
		else
		{$("#g1000-slider-range").slider('enable');}
	  });
	//dbsnp
    $("#id_dbsnp_exclude").click(function(){
		if ($("#id_dbsnp_exclude").is(":checked"))
		{$("#dbsnp-slider-range").slider('disable');}
		else
		{$("#dbsnp-slider-range").slider('enable');}
	  });
  	$("#id_esp_exclude").click(function(){
		if ($("#id_esp_exclude").is(":checked"))
		{$("#esp-slider-range").slider('disable');}
		else
		{$("#esp-slider-range").slider('enable');}
	  });
    
    //Wizard
    //1000genomes
    $( "#g1000-slider-range_wz" ).slider({
            range: true,
            min: 0,
            max: 0.5,
            step: 0.001,
            values: [ 0, 0.5 ],
            slide: function( event, ui ) {  $( "#id_2-genomes1000" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    g1000_value_wz = $("#id_2-genomes1000").val();
    if (g1000_value_wz) {
        value_range =g1000_value_wz.split(" - ");
        $("#g1000-slider-range_wz").slider('values',[value_range[0], value_range[1]]);
    }
    //dbsnp
    $( "#dbsnp-slider-range_wz" ).slider({
            range: true,
            min: 0,
            max: 0.5,
            step: 0.001,
            values: [ 0, 0.5 ],
            slide: function( event, ui ) {  $( "#id_2-dbsnp_frequency" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    dbsnp_value_wz = $("#id_2-dbsnp_frequency").val();
    if (dbsnp_value_wz) {
        value_range =dbsnp_value_wz.split(" - ");
        $("#dbsnp-slider-range_wz").slider('values',[value_range[0], value_range[1]]);
    }
    //esp
    $( "#esp-slider-range_wz" ).slider({
            range: true,
            min: 0,
            max: 0.5,
            step: 0.001,
            values: [ 0, 0.5 ],
            slide: function( event, ui ) {  $( "#id_2-esp_frequency" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    esp_value_wz = $("#id_2-esp_frequency").val();
    if (esp_value_wz) {
        value_range =esp_value_wz.split(" - ");
        $("#esp-slider-range_wz").slider('values',[value_range[0], value_range[1]]);
    }
    //sift
    $( "#sift-slider-range_wz" ).slider({
            range: true,
            min: 0,
            max: 1,
            step: 0.01,
            values: [ 0, 1 ],
            slide: function( event, ui ) {  $( "#id_2-sift" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    sift_value_wz = $("#id_2-sift").val();
    if (sift_value_wz) {
        value_range =sift_value_wz.split(" - ");
        $("#sift-slider-range_wz").slider('values',[value_range[0], value_range[1]]);
    }
    //Polyphen 2
    $( "#pp2-slider-range_wz" ).slider({
            range: true,
            min: 0,
            max: 1,
            step: 0.01,
            values: [ 0, 1 ],
            slide: function( event, ui ) {  $( "#id_2-polyphen" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    pp2_value_wz = $("#id_2-polyphen").val();
    if (pp2_value_wz) {
        value_range =pp2_value_wz.split(" - ");
        $("#pp2-slider-range_wz").slider('values',[value_range[0], value_range[1]]);
    }
    //Mendel,MD Score
    $( "#mendelmd-slider-range_wz" ).slider({
            range: true,
            min: 0,
            max: 12,
            step: 1,
            values: [ 0, 12 ],
            slide: function( event, ui ) {  $( "#id_2-mendelmd_score" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    mendelmd_value_wz = $("#id_2-mendelmd_score").val();
    if (mendelmd_value_wz) {
        value_range =mendelmd_value_wz.split(" - ");
        $("#mendelmd-slider-range_wz").slider('values',[value_range[0], value_range[1]]);
    }
    //Mendel,MD Score Views
    $( "#mendelmd-slider-range" ).slider({
            range: true,
            min: 0,
            max: 12,
            step: 1,
            values: [ 0, 12 ],
            slide: function( event, ui ) {  $( "#id_mendelmd_score" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    mendelmd_value = $("#id_mendelmd_score").val();
    if (mendelmd_value) {
        value_range =mendelmd_value.split(" - ");
        $("#mendelmd-slider-range").slider('values',[value_range[0], value_range[1]]);
    }

    ////////////////One Click
    //1000genomes
    $( "#g1000-slider-range_oc" ).slider({
            range: true,
            min: 0,
            max: 0.5,
            step: 0.001,
            values: [ 0, 0.5 ],
            slide: function( event, ui ) {  $( "#id_genomes1000" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    oneclick_g1000_value = $("#id_genomes1000").val();
    if (oneclick_g1000_value) {
        value_range =oneclick_g1000_value.split(" - ");
        $("#g1000-slider-range_oc").slider('values',[value_range[0], value_range[1]]);
    }
    //dbsnp
    $( "#dbsnp-slider-range_oc" ).slider({
            range: true,
            min: 0,
            max: 0.5,
            step: 0.001,
            values: [ 0, 0.5 ],
            slide: function( event, ui ) {  $( "#id_dbsnp_frequency" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    dbsnp_value_oc = $("#id_dbsnp_frequency").val();
    if (dbsnp_value_oc) {
        value_range =dbsnp_value_oc.split(" - ");
        $("#dbsnp-slider-range_oc").slider('values',[value_range[0], value_range[1]]);
    }
    //esp
    $( "#esp-slider-range_oc" ).slider({
            range: true,
            min: 0,
            max: 0.5,
            step: 0.001,
            values: [ 0, 0.5 ],
            slide: function( event, ui ) {  $( "#id_esp_frequency" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    esp_value_oc = $("#id_esp_frequency").val();
    if (esp_value_oc) {
        value_range =esp_value_oc.split(" - ");
        $("#esp-slider-range_oc").slider('values',[value_range[0], value_range[1]]);
    }
    //sift
    $( "#sift-slider-range_oc" ).slider({
            range: true,
            min: 0,
            max: 1,
            step: 0.01,
            values: [ 0, 1 ],
            slide: function( event, ui ) {  $( "#id_sift" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    sift_value_oc = $("#id_sift").val();
    if (sift_value_oc) {
        value_range =sift_value_oc.split(" - ");
        $("#sift-slider-range_oc").slider('values',[value_range[0], value_range[1]]);
    }
    //Polyphen 2
    $( "#pp2-slider-range_oc" ).slider({
            range: true,
            min: 0,
            max: 1,
            step: 0.01,
            values: [ 0, 1 ],
            slide: function( event, ui ) {  $( "#id_polyphen" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    pp2_value_oc = $("#id_polyphen").val();
    if (pp2_value_oc) {
        value_range =pp2_value_oc.split(" - ");
        $("#pp2-slider-range_oc").slider('values',[value_range[0], value_range[1]]);
    }
    //Mendel,MD Score
    $( "#mendelmd-slider-range_oc" ).slider({
            range: true,
            min: 0,
            max: 12,
            step: 1,
            values: [ 0, 12 ],
            slide: function( event, ui ) {  $( "#id_mendelmd_score" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
            }
    });
    mendelmd_value_oc = $("#id_mendelmd_score").val();
    if (mendelmd_value_oc) {
        value_range =mendelmd_value_oc.split(" - ");
        $("#mendelmd-slider-range_oc").slider('values',[value_range[0], value_range[1]]);
    }


    


});