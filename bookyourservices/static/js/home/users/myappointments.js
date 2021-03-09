import ListAppointments from '/static/js/modules/listAppointments.js';

const APPOINTMENT_LIST_URL = getGlobalValues("APPOINTMENT_LIST_URL");
const APPOINTMENT_UPDATE_URL = getGlobalValues("APPOINTMENT_UPDATE_URL");
const APPOINTMENT_DELETE_URL = getGlobalValues("APPOINTMENT_DELETE_URL");
const APPOINTMENT_PER_PAGE = getGlobalValues("APPOINTMENT_PER_PAGE") ? getGlobalValues("APPOINTMENT_PER_PAGE") : 20;
const $listContainer = $("#appointments-list");
const $form = $("#form-appointment-");
const $newBtn = $("#btn-new");

const listAppointments = new ListAppointments(
    $listContainer,
    $("#appointments-template").html(),
    APPOINTMENT_LIST_URL, 
    APPOINTMENT_PER_PAGE , 
    $form,
    "appointment-");
listAppointments.nameKey = "service";
listAppointments.updateUrl = APPOINTMENT_UPDATE_URL;
listAppointments.deleteUrl = APPOINTMENT_DELETE_URL;

$newBtn.on("click" , (e)=>{
    listAppointments.resetForm();
});

listAppointments.loadList(true , 1 , true);
