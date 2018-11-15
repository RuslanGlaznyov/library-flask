for(var f=document.forms,i=f.length;i--;)f[i].setAttribute("novalidate",i)

//set title input
$('#icon').on('change', function () {
    //get the file name
    var fileName = $(this).val().split('\\');
    fileName = fileName[fileName.length - 1];
    //replace the "Choose a file" label
    console.log(fileName);
    $(this).next('.custom-file-label').html(fileName);
});
$('#book').on('change', function () {
    //get the file name
    var fileName = $(this).val().split('\\');
    fileName = fileName[fileName.length - 1];
    //replace the "Choose a file" label

    $(this).next('.custom-file-label').html(fileName);
});

$('.sb-form').click(function(e) {
    e.target.form.submit()
});