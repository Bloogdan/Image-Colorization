console.log('xD');
Dropzone.options.uploadzone = {
    uploadMultiple: true,
    parallelUploads: 4,
    autoProcessQueue: false,
    maxFiles: 4,
    resizeWidth: 150,
    maxFilesize: 1,
    acceptedFiles: "image/*",

    init: function (e) {
        var myDropzone = this;

        document.querySelector('#btnUpload').onclick = function () {
            myDropzone.processQueue();
        };
    }
};

