$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
    
    $('.actions').on('change', function(){
        var theVal = $(this).val();
        $(".action").addClass('hidden');
        $(".action#"+theVal).removeClass('hidden');
    });

});