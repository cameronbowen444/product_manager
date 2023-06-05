$(document).ready(function(){
    $('#result').hide();
    $('#sendRequest').click(function(){
        $.ajax({
            url: "/dashboard",
            method: "GET"
        })
        .done(function(res){
            $('#category').hide();
            $('#result').show();
        })
    })
    $('#sendBack').click(function(){
        $.ajax({
            url: "/dashboard",
            method: "GET"
        })
        .done(function(res){
            $('#result').hide();
            $('#category').show();
        })
    })
    $('#searched').submit(function(){
        $.ajax({
            url: "/product-search",
            method: "GET",
            data: $('#searched').serialize()
        })
        .done(function(res){
            console.log(res);
            $('#this_product_info').show();
        })
    })
})

function myFunction() {
    var x = document.getElementById("myInput");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}