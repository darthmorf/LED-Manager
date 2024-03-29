$(document).ready(function() {
    $("#coloursubmit").on("click", function() 
    { 
        var colourpicker = $("#colourform");
        var rgb = colourpicker[0].value;

        $.ajax({
			url: '/coloursubmit',
			type: 'POST',
			data: JSON.stringify({ rgb: rgb}),
            // We are using JSON, not XML
			contentType: "application/json; charset=utf-8",
        	dataType: "json",

			success: function(response) {                
                console.log("updated colour");
			},
			error: function(error){
				console.log(error);
			}
		});
    });

	$("#resetcolour").on("click", function() 
    { 
		var colourpicker = $("#colourform");
        var rgb = "rgb(255,167,59)";
		colourpicker[0].jscolor.fromRGBA(255,167,59);

        $.ajax({
			url: '/coloursubmit',
			type: 'POST',
			data: JSON.stringify({ rgb: rgb}),
            // We are using JSON, not XML
			contentType: "application/json; charset=utf-8",
        	dataType: "json",

			success: function(response) {                
                console.log("updated colour");
			},
			error: function(error){
				console.log(error);
			}
		});
    });
});   