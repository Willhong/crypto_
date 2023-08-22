const usdtPriceElement = document.getElementById('usdt-price');
const usdtPriceKRWElement = document.getElementById('usdt-price-krw');

function fetchUSDTPriceInUSD() {
    fetch('https://api.binance.com/api/v3/ticker/price?symbol=BUSDUSDT')
        .then(response => response.json())
        .then(data => {
            const price = parseFloat(data.price).toFixed(7);
            usdtPriceElement.textContent = price.toLocaleString();
            usdtPriceElement.classList.add('flash');
            setTimeout(() => usdtPriceElement.classList.remove('flash'), 1000);
            return price;
        })
        .then(priceInUSD => {
            fetch('https://open.er-api.com/v6/latest/USD')
                .then(response => response.json())
                .then(data => {
                    const rate = data.rates.KRW;
                    const priceInKRW = (priceInUSD * rate).toFixed(7);
                    usdtPriceKRWElement.textContent = priceInKRW.toLocaleString();
                    usdtPriceKRWElement.classList.add('flash');
                    setTimeout(() => usdtPriceKRWElement.classList.remove('flash'), 1000);
                });
        })
        .catch(error => {
            console.error('Error fetching KRW-USD exchange rate:', error);
        });
}

// 처음 페이지 로드 시 환율 정보 가져오기
fetchUSDTPriceInUSD();

// 5초마다 환율 정보 업데이트
setInterval(fetchUSDTPriceInUSD, 10000);