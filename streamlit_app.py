import streamlit as st
from streamlit_javascript import st_javascript

st.title("Hebrew Date Picker")

# HTML and JavaScript code for Hebrew date picker
date_picker_code = """
<!DOCTYPE html>
<html lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@hebcal/core/dist/index.js"></script>
    <script>
        $(function() {
            $.datepicker.regional['he'] = {
                closeText: 'סגור',
                prevText: '&#x3C;הקודם',
                nextText: 'הבא&#x3E;',
                currentText: 'היום',
                monthNames: ['ינואר','פברואר','מרץ','אפריל','מאי','יוני',
                'יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר'],
                monthNamesShort: ['ינו','פבר','מרץ','אפר','מאי','יוני',
                'יולי','אוג','ספט','אוק','נוב','דצמ'],
                dayNames: ['ראשון','שני','שלישי','רביעי','חמישי','שישי','שבת'],
                dayNamesShort: ['א\'','ב\'','ג\'','ד\'','ה\'','ו\'','שבת'],
                dayNamesMin: ['א\'','ב\'','ג\'','ד\'','ה\'','ו\'','שבת'],
                weekHeader: 'Wk',
                dateFormat: 'dd/mm/yy',
                firstDay: 0,
                isRTL: true,
                showMonthAfterYear: false,
                yearSuffix: ''};
            $.datepicker.setDefaults($.datepicker.regional['he']);

            $("#datepicker").datepicker({
                onSelect: function(dateText, inst) {
                    var date = $(this).datepicker('getDate');
                    var hebrewDate = new Hebcal.HDate(date);
                    window.parent.postMessage(hebrewDate.renderGematriya(), "*");
                }
            });
        });
    </script>
</head>
<body>
    <input type="text" id="datepicker" />
</body>
</html>
"""

# Render the date picker
st_javascript(f"""const iframe = document.createElement("iframe");
iframe.setAttribute("srcdoc", `{date_picker_code}`);
iframe.setAttribute("width", "100%");
iframe.setAttribute("height", "400px");
iframe.setAttribute("style", "border: none;");
document.body.appendChild(iframe);

window.addEventListener("message", (event) => {{
    const date = event.data;
    if (date) {{
        document.dispatchEvent(new CustomEvent("date-selected", {{
            detail: date
        }}));
    }}
}});""")

selected_date = st_javascript("return new Promise(resolve => { document.addEventListener('date-selected', (e) => { resolve(e.detail); }); });")

if selected_date:
    st.write("Selected Hebrew Date:", selected_date)
