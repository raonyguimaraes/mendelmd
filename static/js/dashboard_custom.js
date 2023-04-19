 $(document).ready(function(){

 var multipleCancelButton = new Choices('#choices-multiple-remove-button', {
 removeItemButton: true,
 maxItemCount:5,
 searchResultLimit:5,
 renderChoiceLimit:5
 });


 });

 
 jQuery(document).ready(function($) {
		$('.collapse-box > a').click(function(event) {
			if ($(this).find('span').is(':visible')) {
				if($(this).parent().find('.collpase-body').height() == 0) {
					$(this).parent().find('.collpase-body').css('height','auto');
				} else {
					$(this).parent().find('.collpase-body').css('height','0px');	
				}
			}
		});

	});
