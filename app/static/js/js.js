$(document).ready(function() {
    $("#daySubmit").on("click", function() 
    { 
        var colourpicker = $("#dayColourform");
        var rgb = colourpicker[0].value;

		var brightness = $("#dayBrightness")[0].value;
		brightness = parseFloat(brightness);

		if (brightness > 1) {
			brightness = 1;
		}
		else if (brightness < 0) {
			brightness = 0;
		}

        $.ajax({
			url: '/daysubmit',
			type: 'POST',
			data: JSON.stringify({ 
				rgb: rgb,
				brightness: brightness
			}),
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

	$("#nightSubmit").on("click", function() 
    { 
        var colourpicker = $("#nightColourform");
        var rgb = colourpicker[0].value;

		var brightness = $("#nightBrightness")[0].value;
		brightness = parseFloat(brightness);

		if (brightness > 1) {
			brightness = 1;
		}
		else if (brightness < 0) {
			brightness = 0;
		}

		var useNightBrightness = $("#useNightBrightness")[0].checked;

        $.ajax({
			url: '/nightsubmit',
			type: 'POST',
			data: JSON.stringify({ 
				rgb: rgb,
				brightness: brightness,
				useNightBrightness: useNightBrightness
			}),
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

	$("#clearImage").on("click", function() 
	{
		window.location.replace("/reset");
	});

	$("#toggleStrobe").on("click", function() 
    { 
        $.ajax({
			url: '/togglestrobe',
			type: 'POST',
			data: JSON.stringify({}),
            // We are using JSON, not XML
			contentType: "application/json; charset=utf-8",
        	dataType: "json",

			success: function(response) {                
                console.log("strobe");
			},
			error: function(error){
				console.log(error);
			}
		});
    });

	$("#toggleRainbow").on("click", function() 
    { 
        $.ajax({
			url: '/togglerainbow',
			type: 'POST',
			data: JSON.stringify({}),
            // We are using JSON, not XML
			contentType: "application/json; charset=utf-8",
        	dataType: "json",

			success: function(response) {                
                console.log("rainbow");
			},
			error: function(error){
				console.log(error);
			}
		});
    });

	$("#toggleHue").on("click", function() 
    { 
        $.ajax({
			url: '/togglehue',
			type: 'POST',
			data: JSON.stringify({}),
            // We are using JSON, not XML
			contentType: "application/json; charset=utf-8",
        	dataType: "json",

			success: function(response) {                
                console.log("strobe");
			},
			error: function(error){
				console.log(error);
			}
		});
    });
});   