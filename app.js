function fetchUSDTPrice() {
    const endpoint = "https://api.binance.com/api/v3/ticker/price?symbol=USDTUSDC";

    fetch(endpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('usdtPrice').innerText = data.price;
        })
        .catch(error => {
            console.log("There was a problem with the fetch operation:", error.message);
            document.getElementById('usdtPrice').innerText = "Error fetching price";
        });
}


fetchUSDTPrice();
setInterval(fetchUSDTPrice, 10000);
