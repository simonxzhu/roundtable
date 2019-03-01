$(document).ready(function () {
    //@naresh action dynamic childs
    var next = 1;



    $("#add-more").click(function(e){
        e.preventDefault();
        var addto = "#field" + next;
        next = next + 1;
        var newIn = '<div id="field' + next +'"><div class="form-group" name="field'+ next +'"><input type="text" class="form-control" name="rest'+ next +'" placeholder="Paste restaurant_url here" data-rule="minlen:4" data-msg="Please enter at least 8 chars of subject"/><div class="validation"></div></div></div>'
        console.log(newIn);
        var newInput = $(newIn);
        $(addto).after(newInput);
        $("#field" + next).attr('data-source',$(addto).attr('data-source'));
        $("#count").val(next);
    });

    $(".rate-button").on('click', function(event) {
        event.stopPropagation();
        event.stopImmediatePropagation();
        var value = $(this).val();
        cell = value.split(',')
        console.log(cell)
        $(this).parent().children().removeClass('text-light')
        $(this).toggleClass('text-light');
        $.ajax({
            url:'/process_vote',
            type:"get",
            data: {
                'value': value,
            },
            success: function(res) {
                var target_cell = '#rate-average-' + cell[0] + '-' + cell[1]
                console.log(target_cell)
                $(target_cell).html(res)
            }
        })
    });

    $("#search_rest").click(function(){
        var food_type = $('#food_type').val()
        var location = $('#location').val()
        $.ajax({
            url:'/process_search',
            type:"get",
            data: {
                'food_type': food_type,
                'location': location,
            },
            success: function(res){
                $('#rests_map').html(res)
            }
        })
    })

    $(document).on('click', ".add-with-url", function(e){
        console.log("printing printing")

        var rest_url = $(this).val()
        var addto = "#field" + next;
        next = next + 1;
        var newIn = `<div id="field${next}"><div class="form-group" name="field${next}"><input type="text" class="form-control" name="rest${next}" value=${rest_url} data-rule="minlen:4" data-msg="Please enter at least 8 chars of subject"/><div class="validation"></div></div></div>`
        console.log(newIn);
        var newInput = $(newIn);
        $(addto).after(newInput);
        $("#field" + next).attr('data-source',$(addto).attr('data-source'));
        $("#count").val(next);
    });
});

