// MetaMask integration for login/signup
async function handleMetaMaskLoginSignup() {
    if (typeof window.ethereum === 'undefined') {
        alert('MetaMask is not installed!');
        return;
    }
    try {
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        const account = accounts[0];
        // Save to sessionStorage for backend fetch
        sessionStorage.setItem('metamask_account', account);
        // Fetch ETH balance
        const balanceWei = await window.ethereum.request({
            method: 'eth_getBalance',
            params: [account, 'latest']
        });
        const balanceEth = parseFloat(parseInt(balanceWei, 16) / 1e18).toFixed(4);
        sessionStorage.setItem('metamask_balance', balanceEth);
        // Redirect to backend for login/signup
        window.location = '/metamask_auth';
    } catch (err) {
        alert('MetaMask connection failed!');
    }
}

// Attach to button if present
window.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('metamask-connect-btn');
    if (btn) {
        btn.addEventListener('click', handleMetaMaskLoginSignup);
    }
}); 