function show_filter_options(){
    var div_filters = document.getElementsByClassName("filter_options")[0];
    var filters = document.getElementById("filter_options_enable");

    if (filters.checked === true){
        div_filters.style.display = "block";
    } else {
        div_filters.style.display = "none";
    }

    set_input_disability();
}

function set_input_disability(){
    var filters = document.getElementById("filter_options_enable");

    if (filters.checked === false){
        var ingredient_filters = document.getElementsByClassName("ingredient_filter");
        var calorie_filters = document.getElementsByClassName("calorie_filter");
        
        for (let ifil of ingredient_filters){
            ifil.setAttribute("disabled", "");
            ifil.removeAttribute("required");
        }

        for (let cfil of calorie_filters){
            cfil.setAttribute("disabled", "");
            cfil.removeAttribute("required");
        }
    } else {
        var ingredient_filters = document.getElementsByClassName("ingredient_filter");
        var calorie_filters = document.getElementsByClassName("calorie_filter");

        for (let ifil of ingredient_filters){
            ifil.removeAttribute("disabled");
            ifil.setAttribute("required", "");
        }

        for (let cfil of calorie_filters){
            cfil.removeAttribute("disabled");
            cfil.setAttribute("required", "");
        }
    }
}

function add_new_ingredient_filter(){
    var new_filter = document.createElement("INPUT");
    new_filter.setAttribute("type", "text");
    new_filter.setAttribute("placeholder", "Input name of Ingredient to exclude");
    new_filter.required = true;

    var div_ing_filters = document.getElementById("ingredient_filters");
    var count = div_ing_filters.childElementCount;
    new_filter.setAttribute("name", `ingredient_filter_${count}`);
    new_filter.setAttribute("id", `ingredient_filter_${count}`);
    new_filter.setAttribute("class", "ingredient_filter");

    var br = document.createElement("BR");
    br.setAttribute("id", `ingredient_filter_${count}_b1`);
    var br2 = document.createElement("BR");
    br2.setAttribute("id", `ingredient_filter_${count}_b2`);

    div_ing_filters.prepend(br);
    div_ing_filters.prepend(br2);
    div_ing_filters.prepend(new_filter);
}

function remove_ingredient_filter(){
    var div_ing_filters = document.getElementById("ingredient_filters");
    var count = div_ing_filters.childElementCount-3;
    var to_delete = document.getElementById(`ingredient_filter_${count}`);
    var to_delete_b1 = document.getElementById(`ingredient_filter_${count}_b1`);
    var to_delete_b2 = document.getElementById(`ingredient_filter_${count}_b2`);
    to_delete.remove();
    to_delete_b1.remove();
    to_delete_b2.remove();
}

