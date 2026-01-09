// Main JavaScript for Real Estate Analyzer Frontend

let currentPage = 'dashboard';
let currentPropertiesPage = 1;
let decisionChart = null;
let priceChart = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    loadDashboard();
    setupEventListeners();
    loadCityOptions();
});

// Navigation Setup
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const page = this.dataset.page;
            const action = this.dataset.action;
            
            if (page) {
                switchPage(page);
            } else if (action) {
                handleAction(action);
            }
            
            // Update active state
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// Switch between pages
function switchPage(page) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    
    // Show selected page
    const pageElement = document.getElementById(page + '-page');
    if (pageElement) {
        pageElement.classList.add('active');
        currentPage = page;
    }
    
    // Update breadcrumb
    const breadcrumbMap = {
        'dashboard': 'Dashboard',
        'properties': 'Properties',
        'analysis-params': 'Analysis Parameters',
        'filters': 'Filters & Search',
        'rag-chat': 'Chat with AI'
    };
    
    document.getElementById('breadcrumb-text').textContent = breadcrumbMap[page] || 'Page';
    
    // Load page-specific content
    if (page === 'properties') {
        loadProperties();
    } else if (page === 'rag-chat') {
        focusChatInput();
    }
}

// Handle export actions
function handleAction(action) {
    if (action === 'export-csv') {
        window.location.href = '/api/export?format=csv';
    } else if (action === 'export-json') {
        fetch('/api/export?format=json')
            .then(response => response.json())
            .then(data => {
                downloadJSON(data.data, 'properties.json');
            });
    }
}

// Download JSON helper
function downloadJSON(data, filename) {
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(data, null, 2)));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// Load Dashboard
function loadDashboard() {
    fetch('/api/dashboard')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('total-properties').textContent = data.total_properties;
                document.getElementById('buy-recommendations').textContent = data.buy_recommendations;
                document.getElementById('rent-recommendations').textContent = data.rent_recommendations;
                document.getElementById('avg-price').textContent = '₹' + formatNumber(data.avg_price);
                
                // Initialize charts
                initializeDashboardCharts(data);
            }
        })
        .catch(error => console.error('Error loading dashboard:', error));
}

// Initialize Dashboard Charts
function initializeDashboardCharts(data) {
    // Buy vs Rent Chart
    const decisionCtx = document.getElementById('decision-chart').getContext('2d');
    decisionChart = new Chart(decisionCtx, {
        type: 'doughnut',
        data: {
            labels: ['Buy', 'Rent'],
            datasets: [{
                data: [data.buy_recommendations, data.rent_recommendations],
                backgroundColor: ['#2ecc71', '#e74c3c'],
                borderColor: ['#27ae60', '#c0392b'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    
    // Price Distribution Chart
    const priceCtx = document.getElementById('price-chart').getContext('2d');
    priceChart = new Chart(priceCtx, {
        type: 'bar',
        data: {
            labels: ['Avg Price'],
            datasets: [{
                label: 'Price (₹)',
                data: [data.avg_price],
                backgroundColor: '#3498db',
                borderColor: '#2980b9',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            indexAxis: 'y',
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '₹' + formatNumber(value);
                        }
                    }
                }
            }
        }
    });
}

// Load Properties
function loadProperties(page = 1) {
    const city = document.getElementById('city-filter').value;
    const decision = document.getElementById('decision-filter').value;
    const minPrice = document.getElementById('min-price').value;
    const maxPrice = document.getElementById('max-price').value;
    
    let url = `/api/properties?page=${page}&per_page=10`;
    if (city !== 'all') url += `&city=${city}`;
    if (decision !== 'all') url += `&decision=${decision}`;
    if (minPrice) url += `&min_price=${minPrice}`;
    if (maxPrice) url += `&max_price=${maxPrice}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderPropertiesTable(data.data);
                updatePagination(data);
            }
        })
        .catch(error => console.error('Error loading properties:', error));
}

// Render Properties Table
function renderPropertiesTable(properties) {
    const tbody = document.getElementById('properties-tbody');
    
    if (properties.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center">No properties found</td></tr>';
        return;
    }
    
    tbody.innerHTML = properties.map(prop => `
        <tr>
            <td>${prop.location || 'N/A'}</td>
            <td>${prop.city || 'N/A'}</td>
            <td>₹${formatNumber(prop.price)}</td>
            <td>${formatNumber(prop.area_sqft)}</td>
            <td>${prop.bhk || 'N/A'}</td>
            <td>₹${formatNumber(prop.price_per_sqft)}</td>
            <td>₹${formatNumber(prop.wealth_buying)}</td>
            <td>₹${formatNumber(prop.wealth_renting)}</td>
            <td><span class="decision-badge ${prop.decision.toLowerCase()}">${prop.decision}</span></td>
        </tr>
    `).join('');
}

// Update Pagination
function updatePagination(data) {
    currentPropertiesPage = data.page;
    document.getElementById('page-info').textContent = `Page ${data.page} of ${data.total_pages}`;
    
    const prevBtn = document.getElementById('prev-page-btn');
    const nextBtn = document.getElementById('next-page-btn');
    
    prevBtn.disabled = data.page === 1;
    nextBtn.disabled = data.page === data.total_pages;
}

// Load City Options
function loadCityOptions() {
    fetch('/api/city-options')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const select = document.getElementById('city-filter');
                data.cities.forEach(city => {
                    const option = document.createElement('option');
                    option.value = city;
                    option.textContent = city;
                    select.appendChild(option);
                });
            }
        })
        .catch(error => console.error('Error loading cities:', error));
}

// Setup Event Listeners
function setupEventListeners() {
    // Properties filters
    document.getElementById('apply-filters-btn').addEventListener('click', () => {
        currentPropertiesPage = 1;
        loadProperties(1);
    });
    
    document.getElementById('reset-filters-btn').addEventListener('click', () => {
        document.getElementById('city-filter').value = 'all';
        document.getElementById('decision-filter').value = 'all';
        document.getElementById('min-price').value = '';
        document.getElementById('max-price').value = '';
        currentPropertiesPage = 1;
        loadProperties(1);
    });
    
    // Pagination
    document.getElementById('prev-page-btn').addEventListener('click', () => {
        if (currentPropertiesPage > 1) {
            loadProperties(currentPropertiesPage - 1);
        }
    });
    
    document.getElementById('next-page-btn').addEventListener('click', () => {
        loadProperties(currentPropertiesPage + 1);
    });
    
    // Analysis Parameters
    document.getElementById('run-analysis-btn').addEventListener('click', runAnalysis);
    document.getElementById('reset-params-btn').addEventListener('click', resetParameters);
    
    // Chat
    document.getElementById('send-chat-btn').addEventListener('click', sendChatMessage);
    document.getElementById('chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendChatMessage();
    });
}

// Run Analysis
function runAnalysis() {
    const params = {
        down_payment_percent: parseFloat(document.getElementById('down-payment').value),
        loan_rate: parseFloat(document.getElementById('loan-rate').value),
        tax_rate: parseFloat(document.getElementById('tax-rate').value),
        appreciation_rate: parseFloat(document.getElementById('appreciation-rate').value),
        rent_escalation: parseFloat(document.getElementById('rent-escalation').value),
        invest_rate: parseFloat(document.getElementById('invest-rate').value),
        monthly_saving: parseFloat(document.getElementById('monthly-saving').value)
    };
    
    const statusDiv = document.getElementById('analysis-status');
    statusDiv.style.display = 'block';
    document.getElementById('run-analysis-btn').disabled = true;
    
    fetch('/api/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then(data => {
        statusDiv.style.display = 'none';
        document.getElementById('run-analysis-btn').disabled = false;
        
        if (data.success) {
            alert(`Analysis completed!\nTotal Properties: ${data.total_properties}\nBuy: ${data.buy_count}\nRent: ${data.rent_count}`);
            loadDashboard();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        statusDiv.style.display = 'none';
        document.getElementById('run-analysis-btn').disabled = false;
        alert('Error running analysis');
    });
}

// Reset Parameters
function resetParameters() {
    document.getElementById('down-payment').value = '20';
    document.getElementById('loan-rate').value = '8.5';
    document.getElementById('tax-rate').value = '20';
    document.getElementById('appreciation-rate').value = '5';
    document.getElementById('rent-escalation').value = '5';
    document.getElementById('invest-rate').value = '10';
    document.getElementById('monthly-saving').value = '15000';
}

// Send Chat Message
function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addChatMessage(message, 'user');
    input.value = '';
    
    // Send to RAG engine
    fetch('/api/rag-query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: message })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            addChatMessage(data.response, 'bot');
        } else {
            addChatMessage('Sorry, I encountered an error: ' + data.error, 'bot');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addChatMessage('Sorry, I could not process your message.', 'bot');
    });
}

// Add Chat Message
function addChatMessage(text, sender) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.className = `chat-message ${sender}-message`;
    messageElement.innerHTML = `<p>${escapeHtml(text)}</p>`;
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Focus Chat Input
function focusChatInput() {
    document.getElementById('chat-input').focus();
}

// Utility Functions
function formatNumber(num) {
    return Math.round(num).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Add CSS for decision badge
const style = document.createElement('style');
style.textContent = `
    .decision-badge {
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .decision-badge.buy {
        background-color: #d4edda;
        color: #155724;
    }
    
    .decision-badge.rent {
        background-color: #f8d7da;
        color: #721c24;
    }
`;
document.head.appendChild(style);
