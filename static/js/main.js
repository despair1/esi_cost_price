

function delete_blank(product_id){
        $.getJSON("delete_blank.json", {
            product_id : product_id
            }).done(function() {
                $(this).parent().remove()
                var a = "[data-product-id-row='" + product_id+"']"
                $(a).remove()
                console.log($(this))
            })
    }
_.templateSettings = {
  interpolate: /\{\{(.+?)\}\}/g
};
// temp vars: product_id, product_name
var blank_template = _.template(
'<div class="row" data-product-id-row="{{product_id}}">' +
    '<div class="col-lg-9">' +
        '<div data-product-id="{{product_id}}"' +
            'onClick=\'$("#post_product_id").val($(this).attr("data-product-id"));' +
            'document.forms["invisible_form"].submit(); return false;\'>{{product_name}} ' +
        '</div>' +
    '</div>' +
    '<div class="col-lg-2" onclick="delete_blank({{product_id}})">' +
        'Delete' +
    '</div>' +
'</div>' )
$(document).ready(  function() {

    var item;
    function open_product_detail(product_id) {
        $('#post_product_id').val(product_id);
        $('#invisible_form').submit();
    }
    function log( message ) {
      $( "<div>" ).text( message ).attr(
      { 'onClick' : '$("#post_product_id").val($(this).attr("data-product-id"));document.forms["invisible_form"].submit(); return false;',
        'data-product-id' : item.value}).prependTo( "#log" );
      $( "#log" ).scrollTop( 0 );
      //open_product_detail(12)
    }
    function success(data,status,xhr) {
        console.log(data);
        console.log(status);
        if ( data.status == "blank") {
            log( "Selected: " + item.value + " aka " + item.label );
        }
    }
    function insert_blank_product(data,status,xhr) {
        if ( data.status == "blank") {
            $(blank_template({product_id : item.value,
                            product_name: item.label})).prependTo("#log")
        }
    }


    $( "#birds" ).autocomplete({
      source: "item_names.json",
      minLength: 2,
      select: function( event, ui ) {
        item = ui.item;
        $.getJSON("new_product.json", {
        product_id: ui.item.value}, insert_blank_product
        )
        event.preventDefault()
        $("#birds").val("")
      }
    });
  } );