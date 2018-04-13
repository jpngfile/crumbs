$('#file-upload').bind('change', function() {
    var fileName="gbiib";
    console.log("File change");
    fileName = $(this).val();
    $('#file-selected').html(fileName);
})
console.log("Included bind");
