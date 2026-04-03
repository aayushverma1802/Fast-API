document.getElementById('predictBtn').addEventListener('click', async () => {
    const resultDiv = document.getElementById('result');
    
    // Collect the data
    const payload = {
        "inputs_df": [{
            "sepal_length": parseFloat(document.getElementById('sl').value),
            "sepal_width": parseFloat(document.getElementById('sw').value),
            "petal_length": parseFloat(document.getElementById('pl').value),
            "petal_width": parseFloat(document.getElementById('pw').value)
        }]
    };

    resultDiv.innerText = "Processing...";

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        
        // Map ID to Flower Name
        const flowerNames = {0: "Setosa", 1: "Versicolor", 2: "Virginica"};
        const finalName = flowerNames[data.prediction] || "Error";

        resultDiv.innerText = "Species: " + finalName;
    } catch (err) {
        resultDiv.style.color = "#fb7185";
        resultDiv.innerText = "Server Error";
    }
});
