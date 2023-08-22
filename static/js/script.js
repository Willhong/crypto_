const priceElement = document.getElementById('usdt-price');

async function fetchUSDTPriceInKRW() {
    try {
        const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=tether&vs_currencies=krw');
        const data = await response.json();
        const price = parseFloat(data.tether.krw).toFixed(2);
        priceElement.textContent = price.toLocaleString();
        priceElement.classList.add('flash');
        setTimeout(() => priceElement.classList.remove('flash'), 1000);
    } catch (error) {
        console.error('Error fetching USDT price in KRW:', error);
    }
}

// 처음 페이지 로드 시 가격 정보 가져오기
fetchUSDTPriceInKRW();

// 5초마다 가격 정보 업데이트
setInterval(fetchUSDTPriceInKRW, 5000);
