var statusDict = {
    "0": {
        "status": "SKIPPED",
        "cssClass": "text-info"
    },
    "1": {
        "status": "PASSED",
        "cssClass": "text-success"
    },
    "-1": {
        "status": "FAILED",
        "cssClass": "text-danger"
    }
}

var apiObjects = ["projects", "studies", "expressions"];

var singularDict = {
    "projects": "project",
    "studies": "study",
    "expressions": "expression"
};

function capitalize(text) {
    return text.charAt(0).toUpperCase() + text.slice(1);
}

function getSpacer(count) {
    return "-".repeat(count);
}

function getReportLine(element, field_name, field_value) {
    return `<${element}>${field_name}: ${field_value}</${element}>`;
}

function getMatrixCell(cssClass, content) {
    return `<td><span class='${cssClass}'>${content}</span></td>`;
}

function load() {
    
    $.getJSON("temp_result.json", function (data) {
        var text_html = "<h3>Compliance Report Text</h3>";
        var matrix_thead_html = "<tr>"
            + "<th>Server name</th>"
            + "<th>Object and Id</th>"
            + "<th>Test case</th>"
            + "<th>Status</th>"
            + "</tr>";
        var matrix_tbody_html = "";

        var num_reports = data.length;
        var num_tests = data[0].test_results.length;
        
        $.each(data, function (index, report) {
            text_html += getReportLine("h4", "Server name", report.server_name)
                + getReportLine("h4", "Base URL", report.base_url)
                + getReportLine("p", "Total tests", report.total_tests)
                + getReportLine("p", "Total tests passed", 
                                report.total_tests_passed)
                + getReportLine("p", "Total tests failed",
                                report.total_tests_failed)
                + getReportLine("p", "Total tests skipped",
                                report.total_tests_skipped)
                + getReportLine("p", "Total warnings generated",
                                report.total_warnings)
                + getReportLine("h3", report.server_name,
                                "Test result reports");

            $.each(apiObjects, function(index, obj_type) {
                obj_type_title = capitalize(obj_type);
                if (!report.implemented[obj_type]) {
                    obj_type_title += " not implemented for this server";
                }

                text_html += `<h3>${obj_type_title}</h3>`;
                $.each(Object.keys(report.test_results[obj_type]), function(index, obj_id) {
                    text_html += `<h4>${singularDict[obj_type]} id: ${obj_id}</h4>`;

                    $.each(report.test_results[obj_type][obj_id], function (index, result){
                        var cssClass = statusDict[result.result]["cssClass"];
                        var status = statusDict[result.result]["status"];

                        // TEXT REPORT
                        text_html += `<p class='tab1 ${cssClass}'>`
                            + `${result.name}: ${status}</p>`;
                        text_html += "<p class='tab1'>--->" + result.text + "</p>&nbsp;";

                        if(result.edge_cases != 0){
                            var table = '<table style="margin-left:20px" class="table"><thead><tr><th>API</th><th>Result</th></tr></thead><tbody>';
        
                            $.each(result.edge_cases, function(index, edge_case){
                                var row = '<tr><td>';
                                row += edge_case.api + '</td>';
                                if(edge_case.result == 1){
                                    row += '<td class="text-success">PASSED</td></tr>';
                                }
                                else if(edge_case.result == 0 && edge_case.result.warning) {
                                    row += '<td>SKIPPED - WARNING</td></tr>';
                                }
                                else if (edge_case.result == 0 && ! edge_case.result.warning) {
                                    row += '<td>SKIPPED</td></tr>';
                                }
                                else{
                                    row += '<td class="text-warning">FAILED</td></tr>';
                                }
                                table += row;
                            })
                            table += '</tbody></table>';
                            text_html += table;
                        }

                        // MATRIX REPORT
                        var obj_name = singularDict[obj_type];
                        var row = "<tr>"
                            + getMatrixCell(cssClass, report.server_name)
                            + getMatrixCell(
                                cssClass,
                                capitalize(obj_name) + ": " + obj_id
                            )
                            + getMatrixCell(cssClass, result.name)
                            + getMatrixCell(cssClass, status)
                            + "</tr>";
                        matrix_tbody_html += row;
                    });
                })
            })

            text_html += getSpacer(65);
        });

        $("#text").html(text_html);
        $("#compliance_matrix").find("thead").html(matrix_thead_html);
        $("#compliance_matrix").find("tbody").html(matrix_tbody_html);

        var json_container = $('#json');
        json_container
            .jsonPresenter('destroy')
            .jsonPresenter({
                    json: data, // JSON objects here
                });

        var data_str = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));
        $('<a href="data:' + data_str + '" download="data.json"><button style="margin:10px; width:100%" class="btn"><i class="fa fa-download"></i> Download</button></a>').prependTo('#json');
    });
}
