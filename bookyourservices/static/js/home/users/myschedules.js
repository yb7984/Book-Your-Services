import ListSchedules from '/static/js/modules/listSchedules.js';
const CURRENT_USERNAME = getGlobalValues("CURRENT_USERNAME");
const SCHEDULE_LIST_URL = `/api/schedules/${CURRENT_USERNAME}`;
const SCHEDULE_UPDATE_URL = `/api/schedules/${CURRENT_USERNAME}`;
const SCHEDULE_DELETE_URL = `/api/schedules/${CURRENT_USERNAME}/0`;

const $listWeeklyContainer = $("#schedules-list-weekly");
const $listDatesContainer = $("#schedules-list-dates");
const template = $("#schedule-template").html();
const $form = $("#form-schedule-");

//make a counter for how many time has been created
let schedulesCount = 0;

//new button event
$("#btn-new").on("click", async (e) => {
    e.preventDefault();

    const $btn = findClickedButton(e, "btn-new");

    await weeklySchedules.openUpdate($btn);
});

const weeklySchedules = new ListSchedules(
    $listWeeklyContainer,
    template,
    `${SCHEDULE_LIST_URL}/weekly`,
    0,
    $form,
    "schedule-"
);
weeklySchedules.idKey = "date_exp";
weeklySchedules.updateUrl = SCHEDULE_UPDATE_URL;
weeklySchedules.deleteUrl = SCHEDULE_DELETE_URL;

const datesSchedules = new ListSchedules(
    $listDatesContainer,
    template,
    `${SCHEDULE_LIST_URL}/dates`,
    0,
    $form,
    "schedule-"
);
datesSchedules.idKey = "date_exp";
datesSchedules.updateUrl = SCHEDULE_UPDATE_URL;
datesSchedules.deleteUrl = SCHEDULE_DELETE_URL;

weeklySchedules.setReloadList([weeklySchedules , datesSchedules]);
datesSchedules.setReloadList([weeklySchedules , datesSchedules]);


//load all schedules
weeklySchedules.reload();
