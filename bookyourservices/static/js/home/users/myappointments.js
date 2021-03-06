import ListAppointments from '/static/js/modules/listAppointments.js';

const $listContainer = $("#appointments-list");
const $form = $("#form-appointment-");
const $newBtn = $("#btn-new");


const listAppointments = new ListAppointments(
    $listContainer,
    $("#appointments-template").html(),
    APPOINTMENT_LIST_URL, 
    12);

$newBtn.on("click" , (e)=>{
    listAppointments.resetForm();
});

listAppointments.loadList(true , 1 , true);
