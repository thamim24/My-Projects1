// static/js/trip.js
document.addEventListener('DOMContentLoaded', function() {
    const tripForm = document.getElementById('tripForm');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const tripPlan = document.getElementById('tripPlan');
    const tripContent = document.getElementById('tripContent');
    const downloadPdf = document.getElementById('downloadPdf');

    // Set minimum date for date inputs
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('start_date').min = today;
    document.getElementById('end_date').min = today;

    // Update end_date min value when start_date changes
    document.getElementById('start_date').addEventListener('change', function(e) {
        document.getElementById('end_date').min = e.target.value;
        if (document.getElementById('end_date').value < e.target.value) {
            document.getElementById('end_date').value = e.target.value;
        }
    });

    tripForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(tripForm);
        const data = {
            start_location: formData.get('start_location'),
            destination: formData.get('destination'),
            start_date: formData.get('start_date'),
            end_date: formData.get('end_date'),
            budget: {
                amount: parseFloat(formData.get('budget')),
                currency: formData.get('currency')
            }
        };

        // Show loading spinner
        loadingSpinner.classList.remove('hidden');
        tripPlan.classList.add('hidden');

        try {
            const response = await fetch('/plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                // Convert the markdown content to HTML
                tripContent.innerHTML = marked.parse(result.trip_plan);
                tripPlan.classList.remove('hidden');
                downloadPdf.setAttribute('data-trip-id', result.trip_id);
                
                // Update download button href
                downloadPdf.href = `/trip/${result.trip_id}/pdf`;
            } else {
                throw new Error(result.error);
            }
        } catch (error) {
            alert('Error generating trip plan: ' + error.message);
        } finally {
            loadingSpinner.classList.add('hidden');
        }
    });

    // Calculate minimum budget based on destination and duration
    const calculateMinBudget = () => {
        const destination = document.getElementById('destination').value.toLowerCase();
        const startDate = new Date(document.getElementById('start_date').value);
        const endDate = new Date(document.getElementById('end_date').value);
        const currency = document.getElementById('currency').value;
        
        if (!destination || !startDate || !endDate || isNaN(startDate) || isNaN(endDate)) return;

        const days = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;
        const budgetInput = document.getElementById('budget');
        
        // Basic budget calculation
        let baseDaily;
        if (destination.includes('usa') || destination.includes('uk') || destination.includes('europe')) {
            baseDaily = 100;
        } else if (destination.includes('thailand') || destination.includes('malaysia')) {
            baseDaily = 50;
        } else {
            baseDaily = 30;
        }

        // Convert to selected currency
        const rates = {
            'USD': 1,
            'EUR': 0.85,
            'GBP': 0.73,
            'INR': 75
        };

        const minBudget = Math.ceil(baseDaily * days * rates[currency]);
        budgetInput.min = minBudget;
        
        // Only update value if it's empty or less than minimum
        if (!budgetInput.value || parseFloat(budgetInput.value) < minBudget) {
            budgetInput.value = minBudget;
        }
    };

    // Add event listeners for budget calculation
    ['destination', 'start_date', 'end_date', 'currency'].forEach(id => {
        document.getElementById(id).addEventListener('change', calculateMinBudget);
    });
});

