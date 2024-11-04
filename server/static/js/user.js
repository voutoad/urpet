$('#file-input').focus(function() {
    $('label').addClass('focus');
    let files = this.files;
    sendFiles(files);
})
.focusout(function() {
    $('label').removeClass('focus');
});
var dropZone = $('#upload-container');
dropZone.on('drag dragstart dragend dragover dragenter dragleave drop', function(){
    return false;
});
dropZone.on('dragover dragenter', function() {
    dropZone.addClass('dragover');
});
 
dropZone.on('dragleave', function(e) {
    dropZone.removeClass('dragover');
    let dx = e.pageX - dropZone.offset().left;
    let dy = e.pageY - dropZone.offset().top;
    let files = e.originalEvent.dataTransfer.files;
     sendFiles(files);
    if ((dx < 0) || (dx > dropZone.width()) || (dy < 0) || (dy > dropZone.height())) {
        dropZone.removeClass('dragover');
    };
});
function sendFiles(files) {
    let maxFileSize = 5242880;
    let Data = new FormData();
    $(files).each(function(index, file) {
         if ((file.size <= maxFileSize) && ((file.type == 'image/png') || (file.type == 'image/jpeg'))) {
              Data.append('images[]', file);
         }
    });
};
$.ajax({
    url: dropZone.attr('action'),
    type: dropZone.attr('method'),
    data: Data,
    contentType: false,
    processData: false,
    success: function(data) {
         alert('Файлы были успешно загружены');
    }
});