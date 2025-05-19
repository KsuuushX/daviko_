$(document).ready(function(){
    $("a").hover(
        function(){
        $(this).attr("style", "color: black !important;");
    },
        function(){
        $(this).removeAttr("style");
    }
    );
});
