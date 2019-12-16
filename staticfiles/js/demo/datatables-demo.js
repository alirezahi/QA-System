// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({searching: false,paging:false,"language": {
      "emptyTable": "موردی وجود ندارد",
      "info": "داده‌های _START_ تا _END_ از _TOTAL_ مورد"
    }});
});
