function uploadFile(event) {
    event.preventDefault();  // Prevent the form from submitting in the traditional way

    const formData = new FormData();
    const fileInput = document.getElementById('file');
    const file = fileInput.files[0];
    
    if (!file) {
        alert("Please select a file first.");
        return;
    }

    formData.append('file', file);

    fetch('http://127.0.0.1:5001/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const uploadStatus = document.getElementById('uploadStatus');
        uploadStatus.textContent = data.message;

        if (data.message === "File uploaded successfully") {
            uploadStatus.style.color = "green";
        } else {
            uploadStatus.style.color = "red";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        const uploadStatus = document.getElementById('uploadStatus');
        uploadStatus.textContent = "File upload failed.";
        uploadStatus.style.color = "red";
    });
}


function calculateDispersion() {
    const columnName = document.getElementById('dataInput').value;

    if (!columnName) {
        alert("Please enter a column name.");
        return;
    }

    fetch(`http://127.0.0.1:5001/calculate?column=${columnName}`)
        .then(response => {
            console.log('Response Status:', response.status);
            if (!response.ok) {
                throw new Error('Request failed, please check the column name.');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);
            if (data.error) {
                alert(data.error);
                return;
            }

            document.getElementById('standardDeviation').innerText = 'Standard Deviation: ' + data.standard_deviation.toFixed(2);
            document.getElementById('variance').innerText = 'Variance: ' + data.variance.toFixed(2);
            document.getElementById('range').innerText = 'Range: ' + data.range.toFixed(2);
            document.getElementById('interquartileRange').innerText = 'Interquartile Range: ' + data.interquartile_range.toFixed(2);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to calculate. Make sure the API is running and the column name is correct.');
        });
}

function generateBoxPlot() {
    const columnName = document.getElementById('dataInput').value;

    if (!columnName) {
        alert("Please enter a column name.");
        return;
    }

    window.location.href = `http://127.0.0.1:5001/boxplot?column=${columnName}`;
}

function clearFileInput() {
    document.getElementById('file').value = "";
}
