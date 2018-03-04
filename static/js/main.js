$(document).ready(  function() {
    var item;
    function open_product_detail(product_id) {
        $('#post_product_id').val(product_id);
        $('#invisible_form').submit();
    }
    function log( message ) {
      $( "<div>" ).text( message ).attr(
      { 'onClick' : 'document.forms["invisible_form"].submit(); return false;'}).prependTo( "#log" );
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

    $( "#birds" ).autocomplete({
      source: "item_names.json",
      minLength: 2,
      select: function( event, ui ) {
        item = ui.item;
        $.getJSON("new_product.json", {
        product_id: ui.item.value}, success
        )
        event.preventDefault()
        $("#birds").val("")
      }
    });
  } );