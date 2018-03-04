$(document).ready(  function() {
    function log( message ) {
      $( "<div>" ).text( message ).prependTo( "#log" );
      $( "#log" ).scrollTop( 0 );
    }
    function success(data,status,xhr) {
    console.log(data);
    console.log(status);
    console.log(xhr);
    }
    console.log("mmm")
    $( "#birds" ).autocomplete({
      source: "item_names.json",
      minLength: 2,
      select: function( event, ui ) {
        log( "Selected: " + ui.item.value + " aka " + ui.item.label );
        $.getJSON("new_product.json", {
        product_id: ui.item.value}, success
        )
        event.preventDefault()
        $("#birds").val("")
      }
    });
  } );