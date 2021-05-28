let thumbnails = document.getElementsByClassName('thumbnail')

let activeImages = document.getElementsByClassName('active')

for (var i = 0; i < thumbnails.length; i++) {

    thumbnails[i].addEventListener('click', function () {
        console.log(activeImages)

        if (activeImages.length > 0) {
            activeImages[0].classList.remove('active')
        }


        this.classList.add('active')
        document.getElementById('featured').src = this.src
    })
}


let buttonLeft = document.getElementById('prev_card');
let buttonRight = document.getElementById('next_card');

buttonLeft.addEventListener('click', function () {
    for (var i = 0; i < thumbnails.length; i++) {
        // alert(thumbnails[i].className);
        if (thumbnails[i].className === "thumbnail active") {
            /* alert("не jopa") */
            thumbnails[i].classList.remove('active')
            if (thumbnails[i] !== thumbnails[0]) {
                thumbnails[i - 1].classList.add('active')
                document.getElementById('featured').src = thumbnails[i - 1].src
            }
            else {
                thumbnails[thumbnails.length - 1].classList.add('active')
                document.getElementById('featured').src = thumbnails[thumbnails.length - 1].src
            }
            break
        }
    }

})

buttonRight.addEventListener('click', function () {
    for (var i = 0; i < thumbnails.length; i++) {
        /* alert(thumbnails[i].className); */
        if (thumbnails[i].className == "thumbnail active") {
            /* alert("не jopa") */
            thumbnails[i].classList.remove('active')
            if (thumbnails[i] != thumbnails[thumbnails.length - 1]) {
                thumbnails[i + 1].classList.add('active')
                document.getElementById('featured').src = thumbnails[i + 1].src
            }
            else {
                thumbnails[0].classList.add('active')
                document.getElementById('featured').src = thumbnails[0].src
            }
            break
        }
    }
})







/* $('#result_height').html($('input[id="range_height"]').val());

$(document).on('input change', 'input[id="range_height"]', function() {
  $('#result_height').html($(this).val());
}); */




/*    ШИРИНА    */
$('#range_width').bind('input change', function () {
    var data = $('#range_width').val();
    $('#result_width').val(data);
});

$('#result_width').bind('input change', function () {
    var data = $('#result_width').val();
    $('#range_width').val(data);

});

$('#plus_width').click(function () {
    $('#range_width').val(parseInt($('#range_width').val()) + 1);
    $('#result_width').val(parseInt($('#result_width').val()) + 1);
});

$('#minus_width').click(function () {
    $('#range_width').val(parseInt($('#range_width').val()) - 1);
    $('#result_width').val(parseInt($('#result_width').val()) - 1);
});

$(document).click(function () {
    var data = $('#result_width').val();
    if (data < 50) {
        data = 50;
        $('#result_width').val(data);
        $('#range_width').val(data);
    }
    else if (data > 240) {
        data = 240;
        $('#result_width').val(data);
        $('#range_width').val(data);
    }
})


/*    ВЫСОТА    */
$('#range_height').bind('input change', function () {
    var data = $('#range_height').val();
    $('#result_height').val(data);
});

$('#result_height').bind('input change', function () {
    var data = $('#result_height').val();
    $('#range_height').val(data);
});

$('#plus_height').click(function () {
    $('#range_height').val(parseInt($('#range_height').val()) + 1);
    $('#result_height').val(parseInt($('#result_height').val()) + 1);
});

$('#minus_height').click(function () {
    $('#range_height').val(parseInt($('#range_height').val()) - 1);
    $('#result_height').val(parseInt($('#result_height').val()) - 1);
});

$(document).click(function () {
    var data = $('#result_height').val();
    if (data < 120) {
        data = 120;
        $('#result_height').val(data);
        $('#range_height').val(data);
    }
    else if (data > 300) {
        data = 300;
        $('#result_height').val(data);
        $('#range_height').val(data);
    }
})


