var simple_drinks_db = gen_simple_drinks_db();

function map_range(value, low1=0, high1=1, low2=0, high2=100) {
    return parseInt(low2 + (high2 - low2) * (value - low1) / (high1 - low1));
}

function map_instructions(value) {
	return(map_range(value));
}
function gen_drink_steps(drink_id){
	// get ingredients 
	var all_ingredients = drinks_db[drink_id].ingredients;
	var steps = {};
	var pourables = [];
	var extras = []; 

	// split "pourable" and "extras"
	for (var ingredient in all_ingredients) {
		// if ingredient.text contains "Part"
		if (~all_ingredients[ingredient].text.indexOf('Part')) {			
			//insert into pourables array
			var pourable_name = all_ingredients[ingredient].id.split('-').join(' ');
			var pourable_parts = parseInt(all_ingredients[ingredient].text.split(" ")[0]);
			pourables.push({"name":pourable_name,"parts":pourable_parts})
		} else {
			// insert into extras array 
			var extra_name = all_ingredients[ingredient].id.replace('-',' ');
			var amount = all_ingredients[ingredient].textPlain;
			extras.push(amount)
		}	
	}

	// count number of parts. num_parts=count(parts)
	var total_parts = 0; 
	for (var ingredient in pourables) {
		total_parts += pourables[ingredient].parts;
	}
	
	// generate step for each amount between 0 and 100 
	var max = 0;
	for (var ingredient in pourables) {
		var num_parts = pourables[ingredient].parts; 
		var base = max;
		max = base + Math.ceil((100/total_parts) * num_parts);
		for(var i = base; i <= max; i++){
			percent_filled = parseInt(100* (1-(max-i)/(max-base)).toFixed(2));
			steps[i] = {"ingredient": pourables[ingredient].name, "percent_filled":percent_filled};
		}
	}
	steps['extras'] = extras; 
	return steps;
}

function gen_simple_drinks_db() {
	drinks = [];
	for (var drink in drinks_db) {
		
		// gen occasions string
		var occasions = []; 
		for (var occasion in drinks_db[drink].occasions) {
			occasions.push(drinks_db[drink].occasions[occasion].id); 
		}

		var occasions_string = "drink best as a " + occasions.join("/") + " drink";
		
		// gen tastes string 
		var tastes = []; 
		for (var taste in drinks_db[drink].tastes) {
			tastes.push(drinks_db[drink].tastes[taste].id); 
		}
		var taste_string = "drink has a " + tastes.join("/") + " taste";
		
		// gen ingredients strings
		var ingredients = []; 
		for (var ingredient in drinks_db[drink].ingredients) {
			ingredients.push(drinks_db[drink].ingredients[ingredient].textPlain); 
		}
		var ingredients_string = "ingredients: " + ingredients.join(", ");
		
		// compile simple drink description
		var simple_drink_description = {
			'name' : drinks_db[drink].name,
			'occasion' : occasions_string,
			'taste' : taste_string,
			'ingredients' : ingredients_string,
			'id' : drink
		}

		drinks.push(simple_drink_description);
	}
	return drinks; 
}


function stepsForDrink(drink_id,min_range=0,max_range=1) {
    var steps = gen_drink_steps(drink_id);
    return {
    	at: function(value) {
    		return steps[map_range(value,min_range,max_range)]
    	},
    	'extras': steps['extras']
    }
};

//console.log(simple_drinks_db);
//console.log(gen_drink_steps(1));



// simple list of drinks 
	// name
	// description 
		// tastes 
		// alchohol 
		// occasion
		//description plane 
	// ID  
// step by steps 
// [{},{},{}]
// {
// 	name: "alchohol"
// 	quantity: ""
// 	poorable: true/false 
// }
// 