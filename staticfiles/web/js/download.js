async function fetchData() {
    const response = await fetch(apiBaseUrl);
    return await response.json();
}

function downloadCSV() {
    fetchData().then(data => {
        const variableSet = data.variable_set.find(v => v.variable === "No_Smoothing");
        let csvContent = "data:text/csv;charset=utf-8,";
        csvContent += "Formatted Date,Value\n"; // Header
        variableSet.valuedata_set.forEach(item => {
            csvContent += `${item.formatted_date},${item.value}\n`; // Data rows
        });

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "data.csv");
        document.body.appendChild(link); // Required for FF

        link.click(); // This will download the file
        document.body.removeChild(link); // Clean up
    });
}

function downloadExcel() {
    fetchData().then(data => {
        const variableSet = data.variable_set.find(v => v.variable === "No_Smoothing");
        let worksheet = XLSX.utils.json_to_sheet(variableSet.valuedata_set.map(item => ({
            'Formatted Date': item.formatted_date,
            'Value': item.value
        })));
        let workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, "Data");

        // Write to file
        XLSX.writeFile(workbook, "data.xlsx");
    });
}
