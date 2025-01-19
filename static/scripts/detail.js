// Pie Chart using Chart.js with Data Labels


document.addEventListener('DOMContentLoaded', () => {
    GetDetailData().then((resolve, riject) => {
        var ctx = document.getElementById('myPieChart').getContext('2d');
        document.getElementById("msg").textContent = resolve.data.message

        document.getElementById('msg').addEventListener('input', autoResize);

        autoResize();

        let not_confidance = 100 - resolve.data.level_of_confidence
        let data_chart = {
            data: [resolve.data.level_of_confidence.toFixed(3), not_confidance.toFixed(3)],
            backgroundColor: ['#FF4500', '#008080'], // Ubah warna
        }

        if (resolve.data.level_of_confidence >= 100) {
            data_chart = {
                data: [resolve.data.level_of_confidence],
                backgroundColor: ['#FF4500'], // Ubah warna
            }
        }
        var myPieChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Presentasi Tingkat Keyakinan'],
                datasets: [data_chart]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    datalabels: {
                        color: '#fff',
                        formatter: (value) => {
                            return value + '%'; // Display percentage inside the chart
                        },
                        font: {
                            weight: 'bold',
                            size: 16,
                        }
                    }
                }
            },
            plugins: [ChartDataLabels]
        });
    }).catch((riject)=>{
        alert(riject)
        window.location.reload("/login")
    })

})

function GetDetailData() {
    return new Promise((resolve, riject) => {
        const user_id = getLastUrlPart()
        $.ajax({
            type: "GET",
            url: `/detail/data/${user_id}`,
            success: (response) => {
                resolve(response)
            },
            error: (xhr, status, error) => {
                try {
                    const err = JSON.parse(xhr.responseText)
                    if (err.status_code == 500) {
                        window.location.reload("/login")
                    }
                    riject(`[Error: ${err.status_code}] ${err.message}`)
                } catch (er) {
                    riject(`[Error: ${status}] ${error}`)
                }
            }
        });
    })

}

function getLastUrlPart() {
    const currentUrl = window.location.href;
    const parts = currentUrl.split('/');
    return parts.pop() || parts.pop();
}

function autoResize() {
    const textarea = document.getElementById('msg');
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}