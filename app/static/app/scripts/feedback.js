$(document).ready(function(){
    $("input, textarea, select").hover(
        function(){
        $(this).attr("style", "background-color: #fcdff3 !important; border: 1px solid #422617 !important");
    },
        function(){
        $(this).removeAttr("style");
    }
    );
});