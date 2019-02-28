$(document).ready(function () {
    //@naresh action dynamic childs
    var next = 1;
    $("#add-more").click(function(e){
        e.preventDefault();
        var addto = "#field" + next;
        var addRemove = "#field" + (next);
        next = next + 1;
        var newIn = '<div id="field' + next +'"><div class="form-group" name="field'+ next +'"><input type="text" class="form-control" name="rest'+ next +'" placeholder="Paste restaurant_url here" data-rule="minlen:4" data-msg="Please enter at least 8 chars of subject"/><div class="validation"></div></div></div>'
        console.log(newIn);
        var newInput = $(newIn);
        $(addto).after(newInput);
        $("#field" + next).attr('data-source',$(addto).attr('data-source'));
        $("#count").val(next);  
        
            $('.remove-me').click(function(e){
                e.preventDefault();
                var fieldNum = this.id.charAt(this.id.length-1);
                var fieldID = "#field" + fieldNum;
                $(this).remove();
                $(fieldID).remove();
            });
    });

});