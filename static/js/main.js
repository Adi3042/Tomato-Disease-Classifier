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
                // Show the uploaded image
                $('#uploadedImage').attr('src', e.target.result).show();
            }
            reader.readAsDataURL(input.files[0]); // Read the file as a Data URL
        }
    }

    // Trigger file input when the button is clicked
    $("#choose-image-btn").click(function () {
        $("#imageUpload").click(); // Trigger the hidden file input
    });

    // Show image and prediction button on file selection
    $("#imageUpload").change(function () {
        $('.image-section').show(); // Show the image section
        $('#btn-predict').show(); // Show the prediction button
        $('#result').text(''); // Clear previous results
        $('#result').hide(); // Hide results initially
        readURL(this); // Call the readURL function to show the preview
    });

    // Predict button click event
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]); // Create form data

        // Show loading animation
        $(this).hide(); // Hide the predict button during processing
        $('.loader').show(); // Show loading spinner

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false, // Do not set content type
            cache: false, // Do not cache
            processData: false, // Do not process data
            async: true, // Send request asynchronously
            success: function (data) {
                // Get and display the result
                $('.loader').hide(); // Hide loading spinner
                $('#result').fadeIn(600); // Fade in the result area
                $('#result').text('Result: ' + data.result); // Display the prediction result

                console.log('Success!');
            },
            error: function (jqXHR, textStatus, errorThrown) {
                // Handle errors
                $('.loader').hide(); // Hide loading spinner
                $('#result').fadeIn(600); // Show the result area
                $('#result').text('Error: ' + textStatus); // Display error message
                console.error('Error during prediction:', textStatus, errorThrown);
            }
        });
    });
});
