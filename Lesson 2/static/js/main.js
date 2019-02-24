$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                var items = Object.keys(data).map(function(key) {
                    return [key, data[key]];
                });
                // Sort the array based on the second element
                items.sort(function(first, second) {
                    return second[1] - first[1];
                });

                var txt = "";
                txt += "<table>"
                for (x in items) {
                  txt += "<tr><td>" + items[x][0] + "</td><td>" + items[x][1] + "</td></tr>";
                }
                txt += "</table>"
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').html(txt);
                console.log('Success!');
            },
        });
    });

});