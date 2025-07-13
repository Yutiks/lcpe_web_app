document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById('macrosChart');
    if (canvas) {
        const carbs = parseFloat(canvas.dataset.carbs);
        const protein = parseFloat(canvas.dataset.protein);
        const fat = parseFloat(canvas.dataset.fat);

        new Chart(canvas, {
            type: 'doughnut',
            data: {
                labels: ['Carbohydrate', 'Protein', 'Fat'],
                datasets: [{
                    data: [carbs, protein, fat],
                    backgroundColor: [
                        'rgba(255, 77, 136, 0.5)',
                        'rgba(77, 136, 255, 0.5)',
                        'rgba(255, 204, 51, 0.5)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                cutout: '50%',
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }

    const dietSelect = document.getElementById('diet_type');
    if (dietSelect) {
        const form = dietSelect.closest('form');
        dietSelect.addEventListener('change', function () {
            form.submit();
        });
    }
});